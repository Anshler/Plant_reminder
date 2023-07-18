# validation for signup, signin, ...
# this would all be replaced with api call
import yaml
import subprocess
from utils.plant_profile_management import *
from utils.android_port import get_file_path
import requests
# Verify if username and password match/exist
def simple_login_validation(username, password):
    if username == '' or password == '':
        return False, None
    try:
        url = 'http://123.21.72.140:8948/api/v1/auth/login?hl=en'
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        data = {
            'username': username.lower(),
            'email': username.lower(),
            'password': password
        }

        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            # now we update local file content, they're not yet ported to server schema
            content = response.json()
            auth = yaml.safe_load(open(get_file_path('placeholder_server/user/user.yaml'), encoding='utf-8'))
            if auth is None:
                auth = dict()
                plant_list = dict()
                plant_list_advanced = dict()
                plant_calendar = dict()
                cycle = dict()
                calendar_full = dict()
                conversation = dict()

                new_user = 'user0'
            else:
                for user in auth:
                    if auth[user]['email'] == username.lower() or auth[user]['username'] == username.lower():
                        return True, user

                plant_list = retrieve_plant_list()
                plant_list_advanced = retrieve_plant_list_advanced()
                plant_calendar = retrieve_plant_calendar()
                cycle = retrieve_cycle()
                calendar_full = retrieve_calendar_full()
                conversation = retrieve_plant_conversation()

                new_user = 'user' + str(len(auth))

            info = dict()
            info['username'] = content['username']
            info['email'] = content['email']
            info['subscription_status'] = 'free'
            info['energy'] = 50.0
            info['seed'] = 3

            auth[new_user] = info
            plant_list[new_user] = dict()
            plant_list_advanced[new_user] = dict()
            plant_calendar[new_user] = dict()
            cycle[new_user] = dict()
            calendar_full[new_user] = dict()
            conversation[new_user] = dict()

            with open(get_file_path('placeholder_server/user/user.yaml'), 'w', encoding='utf-8') as f:
                yaml.safe_dump(auth, f, sort_keys=False)
            with open(get_file_path('placeholder_server/user/plant_selector.yaml'), 'w', encoding='utf-8') as f:
                yaml.safe_dump(plant_list, f, sort_keys=False)
            with open(get_file_path('placeholder_server/user/plant_selector_advanced.yaml'), 'w',
                      encoding='utf-8') as f:
                yaml.safe_dump(plant_list_advanced, f, sort_keys=False)
            with open(get_file_path('placeholder_server/user/plant_calendar.yaml'), 'w', encoding='utf-8') as f:
                yaml.safe_dump(plant_calendar, f, sort_keys=False)
            with open(get_file_path('placeholder_server/user/cycle.yaml'), 'w', encoding='utf-8') as f:
                yaml.safe_dump(cycle, f)
            with open(get_file_path('placeholder_server/user/calendar_full.yaml'), 'w', encoding='utf-8') as f:
                yaml.safe_dump(calendar_full, f)
            with open(get_file_path('placeholder_server/user/plant_conversation.yaml'), 'w', encoding='utf-8') as f:
                yaml.safe_dump(conversation, f, sort_keys=False)
            return True, new_user
        else:
            return False, None
    except:
        return False, None

# Verify if email exist
def simple_email_validation(email) -> bool:
    if email == '':
        print('Incorrect email')
        return False
    try:
        # This would be an api call
        auth = yaml.safe_load(open(get_file_path('placeholder_server/user/user.yaml'), encoding='utf-8'))
        if auth is None:
            return False
        for user in auth:
            if auth[user]['email'] == email.lower():
                return True
    except: pass
    print('Incorrect email')
    return False

# Verify if new password is different from old
def simple_password_validation(email,password):
    with open(get_file_path('placeholder_server/user/user.yaml'), 'r', encoding='utf-8') as f:
        auth = yaml.safe_load(f)
    for user in auth:
        if auth[user]['email'] == email.lower() and auth[user]['password'] != password:
            auth[user]['password'] = password
            with open(get_file_path('placeholder_server/user/user.yaml'), 'w', encoding='utf-8') as f:
                yaml.safe_dump(auth, f)
            return True, user
    return False, None

# Verify if OTP match
def simple_otp_validation(true_otp, otp) -> bool:
    if true_otp[:6] == otp:
        return True
    return False

def get_otp(email) -> str:
    url = "http://123.21.72.140:8948/otp"  # Replace with the appropriate URL of your Node.js server

    data = {"email": email}
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            return result['otp']
        else:
            print(f"Request failed with status code {response.status_code}")
            return 'ERROR!'
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return 'ERROR!'

def simple_new_user_validation(username,email) -> bool:
    # check if username and email is available
    try:
        url = 'http://123.21.72.140:8948/api/v1/auth/register_validation?hl=en'
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        data = {
            'email': email.lower(),
            'username': username.lower()
        }

        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return None, True
        else: return response.json()['message'], False
    except: return 'Validation failed, try again later', False

def simple_signup_vadilation(username, email, password):
    # actual signup
    try:
        url = 'http://123.21.72.140:8948/api/v1/auth/register?hl=en'
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        data = {
            'email': email.lower(),
            'username': username.lower(),
            'password': password
        }

        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            auth = yaml.safe_load(open(get_file_path('placeholder_server/user/user.yaml'), encoding='utf-8'))
            plant_list = retrieve_plant_list()
            plant_list_advanced = retrieve_plant_list_advanced()
            plant_calendar = retrieve_plant_calendar()
            cycle = retrieve_cycle()
            calendar_full = retrieve_calendar_full()
            conversation = retrieve_plant_conversation()
            if auth is None:
                auth = dict()
                plant_list = dict()
                plant_list_advanced = dict()
                plant_calendar = dict()
                cycle = dict()
                calendar_full = dict()
                conversation = dict()

                new_user = 'user0'
            else:
                new_user = 'user' + str(len(auth))

            info = dict()
            info['username'] = username.lower()
            info['email'] = email.lower()
            info['subscription_status'] = 'free'
            info['energy'] = 50.0
            info['seed'] = 3

            auth[new_user] = info
            plant_list[new_user] = dict()
            plant_list_advanced[new_user] = dict()
            plant_calendar[new_user] = dict()
            cycle[new_user] = dict()
            calendar_full[new_user] = dict()
            conversation[new_user] = dict()

            with open(get_file_path('placeholder_server/user/user.yaml'), 'w', encoding='utf-8') as f:
                yaml.safe_dump(auth, f, sort_keys=False)
            with open(get_file_path('placeholder_server/user/plant_selector.yaml'), 'w', encoding='utf-8') as f:
                yaml.safe_dump(plant_list, f, sort_keys=False)
            with open(get_file_path('placeholder_server/user/plant_selector_advanced.yaml'), 'w', encoding='utf-8') as f:
                yaml.safe_dump(plant_list_advanced, f, sort_keys=False)
            with open(get_file_path('placeholder_server/user/plant_calendar.yaml'), 'w', encoding='utf-8') as f:
                yaml.safe_dump(plant_calendar, f, sort_keys=False)
            with open(get_file_path('placeholder_server/user/cycle.yaml'), 'w', encoding='utf-8') as f:
                yaml.safe_dump(cycle, f)
            with open(get_file_path('placeholder_server/user/calendar_full.yaml'), 'w', encoding='utf-8') as f:
                yaml.safe_dump(calendar_full, f)
            with open(get_file_path('placeholder_server/user/plant_conversation.yaml'), 'w', encoding='utf-8') as f:
                yaml.safe_dump(conversation, f, sort_keys=False)
            return True, new_user
        else:
            return False, ''
    except:
        return False, ''
