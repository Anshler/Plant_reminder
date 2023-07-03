import threading
import yaml
import random
from kivy.utils import platform
from kivy.resources import resource_add_path
if platform == 'android':
    import android
    project_dir = android.PythonActivity.mActivity.getFilesDir().getAbsolutePath()
    resource_add_path(project_dir)
    from utils.calendar_compiler import *
    from virtual_pet.personality import *
    from utils.android_port import get_file_path
else:
    from utils.calendar_compiler import *
    from virtual_pet.personality import *
    from utils.android_port import get_file_path
import uuid
# remove a plant from user profile------------------------------------------------------------------
def simple_remove_key_plant_list(id, plant):
    # update local file
    plant_list = get_plant_list()
    plant_list_advanced = get_plant_list_advanced()
    plant_calendar = get_plant_calendar()
    plant_conversation = get_plant_conversation()

    plant_list.pop(plant)
    plant_list_advanced.pop(plant)
    plant_calendar.pop(plant)
    plant_conversation.pop(plant)

    with open(get_file_path('app_config/local_user_file/plant_selector.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(plant_list, f, sort_keys= False)
    with open(get_file_path('app_config/local_user_file/plant_selector_advanced.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(plant_list_advanced, f, sort_keys= False)
    with open(get_file_path('app_config/local_user_file/plant_calendar.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(plant_calendar, f, sort_keys= False)
    with open(get_file_path('app_config/local_user_file/plant_conversation.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(plant_conversation, f, sort_keys= False)

    # simulated api call
    # this would be an acual api call in the future
    my_thread = threading.Thread(target=simple_remove_key_plant_list_, args=(id,plant))
    my_thread.start()
def simple_remove_key_plant_list_(id, plant):
    # update local file
    plant_list = retrieve_plant_list()
    plant_list_advanced = retrieve_plant_list_advanced()
    plant_calendar = retrieve_plant_calendar()
    plant_conversation = retrieve_plant_conversation()

    plant_list[id].pop(plant)
    plant_list_advanced[id].pop(plant)
    plant_calendar[id].pop(plant)
    plant_conversation[id].pop(plant)

    with open(get_file_path('placeholder_server/user/plant_selector.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(plant_list, f, sort_keys= False)
    with open(get_file_path('placeholder_server/user/plant_selector_advanced.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(plant_list_advanced, f, sort_keys= False)
    with open(get_file_path('placeholder_server/user/plant_calendar.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(plant_calendar, f, sort_keys= False)
    with open(get_file_path('placeholder_server/user/plant_conversation.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(plant_conversation, f, sort_keys= False)

# Add new plant to user profile---------------------------------------------------------------------------
def simple_add_new_plant(id,name,represent_color,avatar,age,date_added,location,extra_notes,result):
    basic = get_plant_list()
    advanced = get_plant_list_advanced()
    calendar = get_plant_calendar()
    conversation = get_plant_conversation()

    if basic is None:
        basic = dict()
        advanced = dict()
        calendar = dict()
        conversation = dict()

    new_plant = str(uuid.uuid4())
    while new_plant in basic:
        new_plant = str(uuid.uuid4())

    info = dict()
    info['name'] = name
    info['represent_color'] = list(represent_color)
    info['avatar'] = avatar
    info['age'] = age
    info['date_added'] = date_added
    info['location'] = location
    info['extra_notes'] = extra_notes

    basic[new_plant] = info
    advanced[new_plant] = result
    calendar[new_plant] = dict()
    conversation[new_plant] = {
        'name': name,
        'positive_trait': random.choice(positive_personality_traits),
        'mundane_trait': random.choice(mundane_personality_traits),
        'flawed_trait': random.choice(flawed_personality_traits),
        'hobby': random.choice(plant_hobbies),
        'manner': random.choice(talking_manners),
        'legacy': list(),
        'recent': list()
    }

    with open(get_file_path('app_config/local_user_file/plant_selector.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(basic, f, sort_keys= False)
    with open(get_file_path('app_config/local_user_file/plant_selector_advanced.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(advanced, f, sort_keys= False)
    with open(get_file_path('app_config/local_user_file/plant_calendar.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(calendar, f, sort_keys= False)
    with open(get_file_path('app_config/local_user_file/plant_conversation.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(conversation, f, sort_keys= False)

    my_thread = threading.Thread(target=simple_add_new_plant_, args=(
        id, name, represent_color, avatar, age, date_added, location, extra_notes, result, new_plant, conversation[new_plant]))
    my_thread.start()
def simple_add_new_plant_(id,name,represent_color,avatar,age,date_added,location,extra_notes,result,new_plant, conversation_trait):
    basic = retrieve_plant_list()
    advanced = retrieve_plant_list_advanced()
    calendar = retrieve_plant_calendar()
    conversation = retrieve_plant_conversation()
    if basic is None:
        basic = dict()
        advanced = dict()
        calendar = dict()
        conversation = dict()

    if id not in basic or basic[id] is None:
        basic[id] = dict()
        advanced[id] = dict()
        calendar[id] = dict()
        conversation[id] = dict()

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
    calendar[id][new_plant] = dict()
    conversation[id][new_plant] = conversation_trait

    with open(get_file_path('placeholder_server/user/plant_selector.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(basic, f, sort_keys= False)
    with open(get_file_path('placeholder_server/user/plant_selector_advanced.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(advanced, f, sort_keys= False)
    with open(get_file_path('placeholder_server/user/plant_calendar.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(calendar, f, sort_keys= False)
    with open(get_file_path('placeholder_server/user/plant_conversation.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(conversation, f, sort_keys= False)

# New user create with empty info------------------------------------------------------------------------
def update_plant_after_signup(id):
    # after sign up, the new user id is created, which is not yet in plant_selection list
    # so we create a relation by adding that new id

    basic = dict()
    advanced = dict()
    calendar = dict()
    conversation = dict()
    cycle = dict()
    calendar_full = dict()

    with open(get_file_path('app_config/local_user_file/plant_selector.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(basic, f, sort_keys= False)
    with open(get_file_path('app_config/local_user_file/plant_selector_advanced.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(advanced, f, sort_keys= False)
    with open(get_file_path('app_config/local_user_file/plant_calendar.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(calendar, f, sort_keys= False)
    with open(get_file_path('app_config/local_user_file/plant_conversation.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(conversation, f,sort_keys= False)
    with open(get_file_path('app_config/local_user_file/cycle.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(cycle, f)
    with open(get_file_path('app_config/local_user_file/calendar_full.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(calendar_full, f)

    # make api call
    update_plant_after_signup_(id)

def update_plant_after_signup_(id):
    # after sign up, the new user id is created, which is not yet in plant_selection list
    # so we create a relation by adding that new id
    # make api call
    basic = retrieve_plant_list()
    advanced = retrieve_plant_list_advanced()
    calendar = retrieve_plant_calendar()
    conversation = retrieve_plant_conversation()
    cycle = retrieve_cycle()
    calendar_full = retrieve_calendar_full()

    if basic is None:
        basic = dict()
        advanced = dict()
        calendar = dict()
        conversation = dict()
        cycle = dict()
        calendar_full = dict()

    basic[id] = dict()
    advanced[id] = dict()
    calendar[id] = dict()
    conversation[id] = dict()
    cycle[id] = dict()
    calendar_full[id] = dict()

    with open(get_file_path('placeholder_server/user/plant_selector.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(basic, f, sort_keys= False)
    with open(get_file_path('placeholder_server/user/plant_selector_advanced.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(advanced, f, sort_keys= False)
    with open(get_file_path('placeholder_server/user/plant_calendar.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(calendar, f, sort_keys= False)
    with open(get_file_path('placeholder_server/user/plant_conversation.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(conversation, f,sort_keys= False)
    with open(get_file_path('placeholder_server/user/cycle.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(cycle,f)
    with open(get_file_path('placeholder_server/user/calendar_full.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(calendar_full,f)

# Edit plant's calendar---------------------------------------------------------------------------------------
def simple_edit_plant_schedule(user_id, plant_id, schedule):
    calendar = get_plant_calendar()
    calendar[plant_id] = schedule

    with open(get_file_path('app_config/local_user_file/plant_calendar.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(calendar, f, sort_keys= False)

    # make api call
    simple_edit_plant_schedule_(user_id,plant_id,schedule)

def simple_edit_plant_schedule_(user_id, plant_id, schedule):
    # api call to update schedule
    calendar = retrieve_plant_calendar()
    calendar[user_id][plant_id] = schedule

    with open(get_file_path('placeholder_server/user/plant_calendar.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(calendar, f, sort_keys= False)
def clean_calendar(calendar):
    if calendar is None: return calendar
    # Only one fertilize in a week
    count = 0
    # Iterate over the entire calendar and remove any dictionary where 'task' is fertilize'
    for key in calendar:
        if isinstance(calendar[key], list):
            items = calendar[key]
            for item in items:
                if 'task' in item:
                    if item['task'] == 'fertilize':
                        count += 1
                        if count > 1:
                            items.remove(item)
                    if item['task'] not in ['water','prune','mist','fertilize']:
                        items.remove(item)
                    if len(str(item['hour'])) != 5:
                        new_hour = str(item['hour']).split(':')
                        new_hour = new_hour[:2]
                        if len(new_hour) == 1:
                            new_hour.append('00')
                        if len(new_hour[0]) != 2:
                            new_hour[0] = '0' + new_hour[0]
                        item['hour'] = ':'.join(new_hour)

                    else:
                        continue
    return calendar
# Save conversation-------------------------------------------------------------------------------
def save_conversation(plant_conversation, id):
    with open(get_file_path('app_config/local_user_file/plant_conversation.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(plant_conversation, f,sort_keys= False)

    # make api call
    my_thread = threading.Thread(target=save_conversation_, args=(plant_conversation, id))
    my_thread.start()
def save_conversation_(plant_conversation, id):
    conversation = retrieve_plant_conversation()
    conversation[id] = plant_conversation
    with open(get_file_path('placeholder_server/user/plant_conversation.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(conversation, f,sort_keys= False)

# Save new item value recalculation --------------------------------------
def save_recalculate(id, change_energy, energy, change_seed, seed, change_subscription_status, subscription_status):
    user = yaml.safe_load(
        open(get_file_path('placeholder_server/user/user.yaml'), encoding='utf-8'))
    if change_energy:
        user[id]['energy'] = energy
    if change_seed:
        user[id]['seed'] = seed
    if change_subscription_status:
        user[id]['subscription_status'] = subscription_status
    with open(get_file_path('placeholder_server/user/user.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(user, f,sort_keys= False)

# api call to retrieve info
def retrieve_plant_list():
    plant_list = yaml.safe_load(open(get_file_path('placeholder_server/user/plant_selector.yaml'), encoding='utf-8'))
    return plant_list
def retrieve_plant_list_advanced():
    plant_list_advanced = yaml.safe_load(open(get_file_path('placeholder_server/user/plant_selector_advanced.yaml'), encoding='utf-8'))
    return plant_list_advanced
def retrieve_plant_calendar():
    plant_calendar = yaml.safe_load(open(get_file_path('placeholder_server/user/plant_calendar.yaml'), encoding='utf-8'))
    return plant_calendar
def retrieve_plant_conversation():
    plant_conversation = yaml.safe_load(open(get_file_path('placeholder_server/user/plant_conversation.yaml'), encoding='utf-8'))
    return plant_conversation
def retrieve_user_info(id):
    user = yaml.safe_load(
        open(get_file_path('placeholder_server/user/user.yaml'), encoding='utf-8'))
    user_info = {'username':user[id]['username'],
                 'subscription_status':user[id]['subscription_status'],
                 'energy':user[id]['energy'],
                 'seed':user[id]['seed']}
    return user_info
def update_current_user(id):
    # make api call to retrieve user info
    plant_list = retrieve_plant_list()
    plant_list_advanced = retrieve_plant_list_advanced()
    plant_calendar = retrieve_plant_calendar()
    plant_conversation = retrieve_plant_conversation()
    cycle = retrieve_cycle()
    calendar_full = retrieve_calendar_full()
    user_info = retrieve_user_info(id)

    # update local file
    meta_config = yaml.safe_load(open(get_file_path('app_config/meta_config.yaml'), encoding='utf-8'))
    meta_config['id'] = id

    with open(get_file_path('app_config/meta_config.yaml'), 'w' ,encoding='utf-8') as f:
        yaml.safe_dump(meta_config, f)
    with open(get_file_path('app_config/local_user_file/plant_selector.yaml'), 'w' ,encoding='utf-8') as f:
        yaml.safe_dump(plant_list[id], f, sort_keys= False)
    with open(get_file_path('app_config/local_user_file/plant_selector_advanced.yaml'), 'w' ,encoding='utf-8') as f:
        yaml.safe_dump(plant_list_advanced[id], f, sort_keys= False)
    with open(get_file_path('app_config/local_user_file/plant_calendar.yaml'), 'w' ,encoding='utf-8') as f:
        yaml.safe_dump(plant_calendar[id], f, sort_keys= False)
    with open(get_file_path('app_config/local_user_file/plant_conversation.yaml'), 'w' ,encoding='utf-8') as f:
        yaml.safe_dump(plant_conversation[id], f,sort_keys= False)
    with open(get_file_path('app_config/local_user_file/cycle.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(cycle[id],f)
    with open(get_file_path('app_config/local_user_file/calendar_full.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(calendar_full[id],f)
    return user_info['username'].capitalize(), user_info['subscription_status'], user_info['energy'], user_info['seed']

# load file from local
def get_plant_list():
    plant_list = yaml.safe_load(open(get_file_path('app_config/local_user_file/plant_selector.yaml'), encoding='utf-8'))
    return plant_list
def get_plant_list_advanced():
    plant_list_advanced = yaml.safe_load(open(get_file_path('app_config/local_user_file/plant_selector_advanced.yaml'), encoding='utf-8'))
    return plant_list_advanced
def get_plant_calendar():
    plant_calendar = yaml.safe_load(open(get_file_path('app_config/local_user_file/plant_calendar.yaml'), encoding='utf-8'))
    return plant_calendar
def get_plant_conversation():
    plant_calendar = yaml.safe_load(
        open(get_file_path('app_config/local_user_file/plant_conversation.yaml'), encoding='utf-8'))
    return plant_calendar
