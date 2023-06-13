import requests

url = 'http://localhost:8928/api/v1/auth/login?hl=en'
payload = {
    'username': 'username2',
    'password': 'string'
}

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

response = requests.post(url, json=payload , headers=headers)
print(response.text)
