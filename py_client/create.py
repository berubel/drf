import requests

token = '03ef67aa9bd807f201415c83dbde509187b6362b'
headers = {
    'Authorization': f'Bearer {token}'
}

endpoint = "http://127.0.0.1:8000/api/products/"

data = {
    "title": "Banana",
    "content":"Fruit", 
    "price": 2.70
}

get_response = requests.post(endpoint, json=data, headers=headers)
# print(get_response.text)
print(get_response.headers)
print(get_response.status_code)
print(get_response.json())
