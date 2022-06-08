import json
import string
import random
from dotenv import dotenv_values
from flask import Flask, Response, redirect, request, render_template
from uplink_python.uplink import Uplink
from uplink_python.errors import StorjException

app = Flask(__name__)
config = dotenv_values('.env')

uplink = Uplink()
access = uplink.request_access_with_passphrase(
    satellite=config['SATELLITE'],
    api_key=config['API_KEY'],
    passphrase=config['PASSPHRASE'],
)
project = access.open_project()


def download_bin(bin_id, bin_size=None):
    try:
        download_file = project.download_object(
            config['BUCKET'], f'{bin_id}.txt')
        if bin_size is None:
            bin_size = 1616
        content = download_file.read(bin_size)[0].decode('utf-8')
        download_file.close()
        return content
    except StorjException:
        return None


@app.route('/')
def index():
    return render_template('pages/index.html')


@app.route('/<bin_id>/')
@app.route('/<bin_id>/<int:bin_size>/')
def download(bin_id, bin_size=None):
    content = download_bin(bin_id, bin_size)
    if content is None:
        return redirect('/')
    return render_template('pages/bin.html', bin_id=bin_id, content=content)


@app.route('/<bin_id>/raw/')
@app.route('/<bin_id>/<int:bin_size>/raw/')
def download_raw(bin_id, bin_size=None):
    return Response(
        download_bin(bin_id, bin_size),
        content_type='text/plain',
    )


@app.route('/upload/', methods=['POST'])
def upload():
    content = request.form.get('content')
    bin_id = ''.join(random.choice(string.ascii_uppercase +
                                   string.ascii_lowercase + string.digits) for _ in range(16))
    upload_file = project.upload_object(config['BUCKET'], f'{bin_id}.txt')
    upload_file.write(bytes(content, 'utf-8'), len(content))
    upload_file.commit()
    res = Response(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                'showMessage': bin_id,
            })
        },
    )
    return res
