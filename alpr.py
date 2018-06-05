import requests
import base64
import json

SECRET_KEY = "sk_b35b858aa12f594a7f6b9525"


def cap():
    IMAGE_PATH = 'plate.jpg'

    with open(IMAGE_PATH, 'rb') as image_file:
        img_base64 = base64.b64encode(image_file.read())
    url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=us&secret_key=%s' % (SECRET_KEY)
    r = requests.post(url, data = img_base64)
    t = json.dumps(r.json(), indent=2)
    return(r.json()["results"][0]['plate'])
