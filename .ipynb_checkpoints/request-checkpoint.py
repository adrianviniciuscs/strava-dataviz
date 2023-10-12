
import requests
import json
# Read the authorization token from a text file
with open('token.txt', 'r') as file:
    authorization_token = file.read().strip()

url = 'https://www.strava.com/api/v3/athlete/activities?per_page=30'
headers = {
    'accept': 'application/json',
    'authorization': f'Bearer {authorization_token}'
}

response = requests.get(url, headers=headers)


data = response.json()
pretty_data = json.dumps(data, indent=4)


print(pretty_data)
