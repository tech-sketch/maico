import requests

url = 'http://localhost:8888/dialog'
data = {'utt': 'Hello'}
res = requests.post(url=url, json=data)
print(res.content)
print(res.cookies.get('session_id'))
for i in range(3):
    cookie = {'session_id': res.cookies.get('session_id')}
    res = requests.post(url=url, json=data, cookies=cookie)
    print(res.cookies.get('session_id'))
    utt = res.json()
    print('sys: {0}'.format(utt['utt']))
