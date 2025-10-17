import requests

BASE = 'http://127.0.0.1:5000'

# register
r = requests.post(f'{BASE}/registry', json={'email':'smoke@example.com','username':'smoke','password':'secret123'})
print('registry', r.status_code, r.text)

# login
r = requests.post(f'{BASE}/login', json={'email':'smoke@example.com','password':'secret123'})
print('login', r.status_code, r.text)

# get users without auth
r = requests.get(f'{BASE}/users')
print('users no auth', r.status_code, r.text)
