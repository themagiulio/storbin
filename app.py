import json
from flask import Flask, Response, request, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('pages/index.html')


@app.route('/upload/', methods=['POST'])
def upload():
    content = request.form.get('content')
    bin_id = 12345
    res = Response(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                'showMessage': f'''Bin successfully uploaded on
                <a href="/bin/{bin_id}" target="_blank">/bin/{bin_id}</a>.''',
            })
        },
    )
    return res
