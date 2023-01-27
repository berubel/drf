import requests
import getpass

auth_endpoint = "http://127.0.0.1:8000/api/auth/"

try:
    username = input('Username: ')
    password = getpass.getpass()
except Exception as error:
    print('ERROR', error)

auth_response = requests.post(auth_endpoint, json={'username':username, 'password': password})
print(auth_response.json())

if auth_response.status_code == 200:
    token = auth_response.json()['token']
    headers = {'Authorization': f'Bearer {token}'}

    endpoint = "http://127.0.0.1:8000/api/products/"

    get_response = requests.get(endpoint, headers=headers)
    data = get_response.json()

    next_url = data['next']
    results = data['results']
    print(next_url)
    print(results)

    # if next_url is not None:
    #     get_response = requests.get(next_url, headers=headers)
    #     print(get_response.json())
  