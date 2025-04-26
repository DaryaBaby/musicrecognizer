from flask import Flask, request, jsonify
import requests
import time
import hashlib
import base64
import hmac

app = Flask(__name__)

@app.route("/recognize", methods=["POST"])
def recognize():
    audio_file = request.files['file']
    audio_data = audio_file.read()

    access_key = "6ac67c7ade89f7d615bc819638b2c31d"
    access_secret = "XB2S30PIzu8XiAiIfJYmfFpRzDHqDWVXztezslem"
    requrl = "http://identify-eu-west-1.acrcloud.com/v1/identify"
    http_method = "POST"
    http_uri = "/v1/identify"
    data_type = "audio"
    signature_version = "1"
    timestamp = str(int(time.time()))

    string_to_sign = "\n".join([http_method, http_uri, access_key, data_type, signature_version, timestamp])
    sign = base64.b64encode(hmac.new(access_secret.encode(), string_to_sign.encode(), digestmod=hashlib.sha1).digest()).decode()

    files = {
        'sample': audio_data,
    }

    data = {
        'access_key': access_key,
        'data_type': data_type,
        'signature_version': signature_version,
        'signature': sign,
        'sample_bytes': len(audio_data),
        'timestamp': timestamp
    }

    response = requests.post(requrl, files=files, data=data)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run()
