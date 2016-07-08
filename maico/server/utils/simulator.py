import requests

url = 'http://localhost:8080/dialog'
data = {'usr_utt': 'はい'}
res = requests.post(url=url, json=data)
print(res.content)
print(res.cookies.get('session_id'))
for i in range(3):
    cookie = {'session_id': res.cookies.get('session_id')}
    res = requests.post(url=url, json=data, cookies=cookie)
    print(res.cookies.get('session_id'))
    utt = res.json()
    print('sys: {0}'.format(utt['utt']))
