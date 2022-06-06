# Storbin

A webapp for uploading and downloading text files on Storj decentralized cloud.

## Instructions

1. Install required packages.
    
    ```
    $ pip install -r requirements.txt
    ```

2. Create a `.env` file and set the following variables.

    ```
    SATELLITE = "satellite url"
    API_KEY = "your api key"
    PASSPHRASE = "your passphrase"
    BUCKET = "your bucket name"
    ```
  
    `SATELLITE` and `API_KEY` can be found using the uplink CLI:

    ```
    $ uplink access inspect
    ```

3. Run development server.

    ```
    $ flask run
    ```