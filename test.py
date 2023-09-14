import base64
from io import BytesIO
import requests
from PIL import Image


def backend_requests_get(url):
    headers = {'Connection': 'close', 'token': 'pass'}
    response = requests.get(url=url, headers=headers)
    json_data = response.json()
    return json_data


def backend_requests_post(url, json):
    headers = {'Connection': 'close', 'token': 'pass'}
    response = requests.post(url=url, json=json, headers=headers)
    json_data = response.json()
    return json_data


server = '45.253.64.78:7860'
# server = '127.0.0.1:7860'

with open('images/face3.png', 'rb') as f:
    content = f.read()

content = base64.b64encode(content)
content = content.decode()

ret = backend_requests_post(url=f'http://{server}/api/auto_flag', json={
    'image': content,
    'alpha': 0.7,

})

byte_data = base64.b64decode(ret.get('image'))  # base64转二
image = Image.open(BytesIO(byte_data))  # 将二进制转为PIL格式图片
image.show()
