# pinata_utils.py
import requests

PINATA_API_KEY = '71afbf8220063f826a81'
PINATA_SECRET_API_KEY = '21b43d253bfc28bfbee4e534af13c34c7a32605337819f0a037a19364ea32822'

def upload_to_pinata(file_path):
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_SECRET_API_KEY
    }

    with open(file_path, 'rb') as file:
        response = requests.post(url, files={"file": file}, headers=headers)
        if response.status_code == 200:
            return response.json()["IpfsHash"]
        else:
            raise Exception("Failed to upload to Pinata: " + response.text)



