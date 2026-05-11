import requests

TOKEN = '8611639719:AAGkYy7e3sVqAn4Ozy6YOKhtqe-70wPUHls'
CHAT_ID = '8759965133'

url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

data = {
    'chat_id': CHAT_ID,
    'text': '텔레그램 테스트 성공'
}

response = requests.post(url, data=data)

print(response.text)