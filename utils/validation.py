# validation for signup, signin, ...
# this would all be replaced with api call

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
        return False, None
    try:
        # This would be an api call
        auth = yaml.safe_load(open('placeholder_server/user/user.yaml', encoding='utf-8'))
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
        auth = yaml.safe_load(open('placeholder_server/user/user.yaml', encoding='utf-8'))
        if auth is None:
            return False
        for user in auth:
            if auth[user]['email'] == email.lower():
                return True
    except: pass
    print('Incorrect email')
    return False

# Verify if new password is different from old
def simple_password_validation(email,password) -> bool:
    with open('placeholder_server/user/user.yaml', 'r', encoding='utf-8') as f:
        auth = yaml.safe_load(f)
    for user in auth:
        if auth[user]['email'] == email.lower() and auth[user]['password'] != password:
            auth[user]['password'] = password
            with open('placeholder_server/user/user.yaml', 'w', encoding='utf-8') as f:
                yaml.safe_dump(auth, f)
            return True, user
    return False, None

# Verify if OTP match
def simple_otp_validation(text) -> bool:
    otp = open(resources.path('placeholder_server','otp.txt')).read()
    if text == otp:
        return True
    return False

def get_otp():
    # Call the OTP program as a separate process
    subprocess.Popen("python " + str(resources.path('utils', 'otp_generator.py')))

def simple_new_user_validation(username) -> bool:
    # This would be an api call
    try:
        auth = yaml.safe_load(open('placeholder_server/user/user.yaml', encoding='utf-8'))
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
        auth = yaml.safe_load(open('placeholder_server/user/user.yaml', encoding='utf-8'))
        if auth is None:
            return True
        for user in auth:
            if auth[user]['email'] == email.lower():
                return False
    except: return False
    return True

def simple_signup_vadilation(username, email, password):
    # This would be an api call
    auth = yaml.safe_load(open('placeholder_server/user/user.yaml', encoding='utf-8'))
    if auth is None:
        auth = dict()
        new_user = 'user0'
    else:
        new_user = 'user'+str(len(auth))

    info = dict()
    info['username'] = username.lower()
    info['email'] = email.lower()
    info['password'] = password
    auth[new_user]=info
    with open('placeholder_server/user/user.yaml', 'w', encoding='utf-8') as f:
        yaml.safe_dump(auth, f)
    return new_user

def simple_remove_key__plant_list(id, plant):
    plant_list = get_plant_list()
    advanced_plant_list = get_advanced_plant_list()

    plant_list[id].pop(plant)
    advanced_plant_list[id].pop(plant)

    new_plant_list = continuous_numbering(plant_list[id])
    new_advanced_plant_list = continuous_numbering(advanced_plant_list[id])

    plant_list[id]=new_plant_list
    advanced_plant_list[id]=new_advanced_plant_list

    with open('placeholder_server/user/plant_selector.yaml', 'w', encoding='utf-8') as f:
        yaml.safe_dump(plant_list, f)
    with open('placeholder_server/user/plant_selector_advanced.yaml', 'w', encoding='utf-8') as f:
        yaml.safe_dump(advanced_plant_list, f)

def continuous_numbering(data):
    # Update key names to maintain continuous numbering
    updated_data = {}
    for i, (key, value) in enumerate(data.items()):
        new_key = f"plant{i}"
        updated_data[new_key] = value
    return updated_data
def simple_add_new_plant(id,name,represent_color,avatar,age,date_added,location,extra_notes, result):
    # This would be an api call
    basic = yaml.safe_load(open('placeholder_server/user/plant_selector.yaml', encoding='utf-8'))
    advanced = yaml.safe_load(open('placeholder_server/user/plant_selector_advanced.yaml', encoding='utf-8'))

    if basic is None:
        basic = dict()
        basic[id] = dict()
        advanced = dict()
        advanced[id] = dict()

        new_plant = 'plant0'

    elif id not in basic or basic[id] is None:
        basic[id] = dict()
        advanced[id] = dict()

        new_plant = 'plant0'
    else:
        new_plant = 'plant' + str(len(basic[id]))

    info = dict()
    info['name'] = name
    info['represent_color'] = list(represent_color)
    info['avatar'] = avatar
    info['age'] = age
    info['date_added'] = date_added
    info['location'] = location
    info['extra_notes'] = extra_notes

    basic[id][new_plant] = info
    advanced[id][new_plant] = result

    with open('placeholder_server/user/plant_selector.yaml', 'w', encoding='utf-8') as f:
        yaml.safe_dump(basic, f)
    with open('placeholder_server/user/plant_selector_advanced.yaml', 'w', encoding='utf-8') as f:
        yaml.safe_dump(advanced, f)
def update_plant_after_signup(id):
    # after sign up, the new user id is created, which is not yet in plant_selection list
    # so we create a relation by adding that new id
    basic = yaml.safe_load(open('placeholder_server/user/plant_selector.yaml', encoding='utf-8'))
    advanced = yaml.safe_load(open('placeholder_server/user/plant_selector_advanced.yaml', encoding='utf-8'))

    if basic is None:
        basic = dict()
        advanced = dict()
    basic[id] = dict()
    advanced[id] = dict()
    with open('placeholder_server/user/plant_selector.yaml', 'w', encoding='utf-8') as f:
        yaml.safe_dump(basic, f)
    with open('placeholder_server/user/plant_selector_advanced.yaml', 'w', encoding='utf-8') as f:
        yaml.safe_dump(advanced, f)
def get_plant_list():
    plant_list = yaml.safe_load(open(resources.path('placeholder_server.user', 'plant_selector.yaml'), encoding='utf-8'))
    return plant_list
def get_advanced_plant_list():
    advanced_plant_list = yaml.safe_load(open(resources.path('placeholder_server.user', 'plant_selector_advanced.yaml'), encoding='utf-8'))
    return advanced_plant_list

def update_current_user(id):
    meta_config = yaml.safe_load(open(resources.path('app_config', 'meta_config.yaml'), encoding='utf-8'))
    meta_config['id'] = id
    with open(resources.path('app_config', 'meta_config.yaml'), 'w' ,encoding='utf-8') as f:
        yaml.safe_dump(meta_config, f)
