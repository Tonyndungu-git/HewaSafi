import requests
import sys
from getpass import getpass

#city = sys.argv[1]

username = input("Username: ")
password = getpass("Password: ")
auth_endpoint = "http://localhost:8000/api/auth/"

# Authenticate and get the token
auth_response = requests.post(auth_endpoint, json={"username": username, "password": password})
auth_data = auth_response.json()
token = auth_data.get("token")
print(token)

if auth_response.status_code == 200 and token:
    air_quality_endpoint = f"http://localhost:8000/api/airquality/"

    headers = {"Authorization": f"Token {token}"}

    get_response = requests.get(air_quality_endpoint, headers=headers)

    if get_response.status_code == 200:
        print(get_response.headers)
    else:
        print(f"Failed to fetch air quality data: {get_response.status_code}")
else:
    print("Authentication failed")
