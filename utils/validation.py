# this would all be api call
try:
    from importlib import resources
except ImportError:
    import importlib_resources as resources
import yaml
import subprocess

# Verify if username and password match/exist
def simple_login_validation(username, password) -> bool:
    if username == '' or password == '':
        print('can\'t login')
        return False
    try:
        # This would be an api call
        auth = yaml.safe_load(open('placeholder_server/user/user.yaml', encoding='utf-8'))
        for user in auth:
            if auth[user]['username'].lower() == username.lower() and auth[user]['password'] == password:
                return True
            if auth[user]['email'].lower() == username.lower() and auth[user]['password'] == password:
                return True
    except:
        pass
    print('can\'t login')
    return False

# Verify if email exist
def simple_email_validation(email) -> bool:
    if email == '':
        print('Incorrect email')
        return False
    try:
        # This would be an api call
        auth = yaml.safe_load(open('placeholder_server/user/user.yaml', encoding='utf-8'))
        for user in auth:
            if auth[user]['email'].lower() == email.lower():
                return True
    except: pass
    print('Incorrect email')
    return False

# Verify if new password is different from old
def simple_password_validation(email,password) -> bool:
    with open('placeholder_server/user/user.yaml', 'r', encoding='utf-8') as f:
        auth = yaml.safe_load(f)
    for user in auth:
        if auth[user]['email'].lower() == email.lower() and auth[user]['password'] != password:
            auth[user]['password'] = password
            with open('placeholder_server/user/user.yaml', 'w', encoding='utf-8') as f:
                yaml.safe_dump(auth, f)
            return True
    return False

# Verify if OTP match
def simple_otp_validation(text) -> bool:
    otp = open(resources.path('placeholder_server','otp.txt')).read()
    if text == otp:
        return True
    return False

def get_otp():
    # Call the OTP program as a separate process
    subprocess.Popen("python " + str(resources.path('utils', 'otp_generator.py')))