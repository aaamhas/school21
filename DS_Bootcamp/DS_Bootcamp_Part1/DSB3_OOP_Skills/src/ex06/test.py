import requests, config
url = f'https://api.telegram.org/bot{config.token}/sendMessage'
r = requests.post(url, data={'chat_id': config.chat_id, 'text': 'test'})
print(r.status_code)
print(r.text)