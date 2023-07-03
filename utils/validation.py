# validation for signup, signin, ...
# this would all be replaced with api call
import yaml
import subprocess
from kivy.utils import platform
from kivy.resources import resource_add_path
if platform == 'android':
    import android
    project_dir = android.PythonActivity.mActivity.getFilesDir().getAbsolutePath()
    resource_add_path(project_dir)
    from utils.plant_profile_management import *
    from utils.android_port import get_file_path
else:
    from utils.plant_profile_management import *
    from utils.android_port import get_file_path

# Verify if username and password match/exist
def simple_login_validation(username, password):
    if username == '' or password == '':
        print('can\'t login')
        return False, None
    try:
        # This would be an api call
        auth = yaml.safe_load(open(get_file_path('placeholder_server/user/user.yaml'), encoding='utf-8'))
        if auth is None:
            return False,None
        for user in auth:
            if auth[user]['username'] == username.lower() and auth[user]['password'] == password:
                return True, user
            if auth[user]['email'] == username.lower() and auth[user]['password'] == password:
                return True, user
    except:
        pass
    print('can\'t login')
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
def simple_otp_validation(text) -> bool:
    otp = open(get_file_path('placeholder_server/otp.txt')).read()
    if text == otp:
        return True
    return False

def get_otp():
    # Call the OTP program as a separate process
    subprocess.Popen("python " + str(get_file_path('utils/otp_generator.py')))

def simple_new_user_validation(username) -> bool:
    # This would be an api call
    try:
        auth = yaml.safe_load(open(get_file_path('placeholder_server/user/user.yaml'), encoding='utf-8'))
        if auth is None:
            return True
        for user in auth:
            if auth[user]['username'] == username.lower():
                return False
    except: return False
    return True
def simple_new_email_validation(email) -> bool:
    # This would be an api call
    try:
        auth = yaml.safe_load(open(get_file_path('placeholder_server/user/user.yaml'), encoding='utf-8'))
        if auth is None:
            return True
        for user in auth:
            if auth[user]['email'] == email.lower():
                return False
    except: return False
    return True

def simple_signup_vadilation(username, email, password):
    # This would be an api call
    auth = yaml.safe_load(open(get_file_path('placeholder_server/user/user.yaml'), encoding='utf-8'))
    plant_list = retrieve_plant_list()
    plant_list_advanced = retrieve_plant_list_advanced()
    plant_calendar = retrieve_plant_calendar()
    cycle = retrieve_cycle()
    calendar_full = retrieve_calendar_full()
    if auth is None:
        auth = dict()
        plant_list = dict()
        plant_list_advanced = dict()
        plant_calendar = dict()
        cycle = dict()
        plant_calendar = dict()

        new_user = 'user0'
    else:
        new_user = 'user'+str(len(auth))

    info = dict()
    info['username'] = username.lower()
    info['email'] = email.lower()
    info['password'] = password
    info['subscription_status'] = 'free'
    info['energy'] = 50.0
    info['seed'] = 3

    auth[new_user]=info
    plant_list[new_user] = dict()
    plant_list_advanced[new_user] = dict()
    plant_calendar[new_user] = dict()
    cycle[new_user] = dict()
    calendar_full[new_user] = dict()

    with open(get_file_path('placeholder_server/user/user.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(auth, f, sort_keys= False)
    with open(get_file_path('placeholder_server/user/plant_selector.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(plant_list, f, sort_keys= False)
    with open(get_file_path('placeholder_server/user/plant_selector_advanced.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(plant_list_advanced, f, sort_keys= False)
    with open(get_file_path('placeholder_server/user/plant_calendar.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(plant_calendar, f, sort_keys= False)
    with open(get_file_path('placeholder_server/user/cycle.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(cycle,f)
    with open(get_file_path('placeholder_server/user/calendar_full.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(calendar_full,f)
    return new_user
