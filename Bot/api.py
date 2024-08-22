import requests
import json

BASE_URL = "http://127.0.0.1:8000"


def is_code_unique(code):
    users = get_all_users()
    return not any(user['code'] == code for user in users)

def create_user(username, name, user_id, contact, code):
    if not is_code_unique(code):
        return "The code is repeating, please press /login or try again in 1 minute!"

    url = f"{BASE_URL}/bot-users/list/"
    response = requests.get(url=url)

    if response.status_code == 200:
        data = response.json()
        user_exist = any(i["user_id"] == user_id for i in data)

        if not user_exist:
            post_url = f"{BASE_URL}/bot-users/"
            post_response = requests.post(
                url=post_url,
                data={'username': username, 'name': name, 'user_id': user_id, 'contact': contact, 'code': code})

            if post_response.status_code == 201:
                return "User created"
            else:
                return f"There was an error creating the user: {post_response.status_code}"
        else:
            return "User exists"
    else:
        return f"An error occurred while retrieving users. Status code: {response.status_code}"

def update_user(user_id, code):
    if not is_code_unique(code):
        return "The code is repeating, please press /login or try again in 1 minute!"

    url = f"{BASE_URL}/bot-users/update/{user_id}/"

    response = requests.patch(url=url, json={'code': code})
    if response.status_code == 200:
        return "User information updated!"
    else:
        return f"FThere was an error updating the driver : {response.status_code}, {response.text}"



def get_all_users():
    url = f"{BASE_URL}/bot-users/list/"
    response = requests.get(url=url)
    if response.status_code == 200:
        return response.json()
    else:
        return None