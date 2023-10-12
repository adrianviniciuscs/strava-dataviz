import requests
import json
import os


def checkAPIKeys():

    with open('refresh_token.txt', 'r') as file:
        refresh_token = file.read().strip()

    client_id = os.environ.get('STRAVA_CID')
    client_secret = os.environ.get('STRAVA_SKEY')

    url = 'https://www.strava.com/api/v3/oauth/token'         
    payload = {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
            }

    response = requests.post(url, data=payload)

    if response.status_code == 200:

        response_data = response.json()  

        access_token = response_data['access_token']
        refresh_token = response_data['refresh_token']

        with open('token.txt', 'w') as file:
            file.write(access_token)

        with open('refresh_token.txt', 'w') as file:
            file.write(refresh_token)
            print("API Keys updated")
    else:
        print(f"Error updating API Keys. Status code: {response.status_code}")


def requestStravaAPI():
    with open('token.txt', 'r') as file:
        authorization_token = file.read().strip()

    url = 'https://www.strava.com/api/v3/athlete/activities'
    headers = {
        'accept': 'application/json',
        'authorization': f'Bearer {authorization_token}'
    }

    data = []
    page = 1

    while True:
        page_url = f'{url}?&page={page}'
        response = requests.get(page_url, headers=headers)

        if response.status_code == 200:
            tempData = response.json()

            if not tempData:
                print("End ofpages!")
                break

            data.extend(tempData)
            page += 1
            print(f'Parsed page n {page}')
        else:
            print(f"Error fetching activities. Status code:{response.status_code}")
            break
    return data
