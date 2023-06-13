import threading
try:
    from importlib import resources
except ImportError:
    import importlib_resources as resources
import yaml
from utils.calendar_compiler import *
# remove a plant from user profile------------------------------------------------------------------
def simple_remove_key_plant_list(id, plant):
    # update local file
    plant_list = get_plant_list()
    plant_list_advanced = get_plant_list_advanced()
    plant_calendar = get_plant_calendar()

    plant_list.pop(plant)
    plant_list_advanced.pop(plant)
    plant_calendar.pop(plant)

    plant_list = continuous_numbering(plant_list)
    plant_list_advanced = continuous_numbering(plant_list_advanced)
    plant_calendar = continuous_numbering(plant_calendar)

    with open(resources.path('app_config.local_user_file', 'plant_selector.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(plant_list, f)
    with open(resources.path('app_config.local_user_file', 'plant_selector_advanced.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(plant_list_advanced, f)
    with open(resources.path('app_config.local_user_file', 'plant_calendar.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(plant_calendar, f)

    # simulated api call
    # this would be an acual api call in the future
    my_thread = threading.Thread(target=simple_remove_key_plant_list_, args=(id,plant))
    my_thread.start()
def simple_remove_key_plant_list_(id, plant):
    # update local file
    plant_list = retrieve_plant_list()
    plant_list_advanced = retrieve_plant_list_advanced()
    plant_calendar = retrieve_plant_calendar()

    plant_list[id].pop(plant)
    plant_list_advanced[id].pop(plant)
    plant_calendar[id].pop(plant)

    plant_list[id] = continuous_numbering(plant_list[id])
    plant_list_advanced[id] = continuous_numbering(plant_list_advanced[id])
    plant_calendar[id] = continuous_numbering(plant_calendar[id])

    with open(resources.path('placeholder_server.user', 'plant_selector.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(plant_list, f)
    with open(resources.path('placeholder_server.user', 'plant_selector_advanced.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(plant_list_advanced, f)
    with open(resources.path('placeholder_server.user', 'plant_calendar.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(plant_calendar, f)
def continuous_numbering(data):
    # Update plant's key name to maintain continuous numbering
    updated_data = {}
    for i, (key, value) in enumerate(data.items()):
        new_key = f"plant{i}"
        updated_data[new_key] = value
    return updated_data

# Add new plant to user profile---------------------------------------------------------------------------
def simple_add_new_plant(id,name,represent_color,avatar,age,date_added,location,extra_notes,result,schedule):
    basic = get_plant_list()
    advanced = get_plant_list_advanced()
    calendar = get_plant_calendar()

    if basic is None:
        basic = dict()
        advanced = dict()
        calendar = dict()
        new_plant = 'plant0'
    else:
        new_plant = 'plant' + str(len(basic))

    info = dict()
    info['name'] = name
    info['represent_color'] = list(represent_color)
    info['avatar'] = avatar
    info['age'] = age
    info['date_added'] = date_added
    info['location'] = location
    info['extra_notes'] = extra_notes

    if schedule is not None and schedule != {}:
        schedule = clean_calendar(schedule)

    basic[new_plant] = info
    advanced[new_plant] = result
    calendar[new_plant] = schedule

    with open(resources.path('app_config.local_user_file', 'plant_selector.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(basic, f)
    with open(resources.path('app_config.local_user_file', 'plant_selector_advanced.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(advanced, f)
    with open(resources.path('app_config.local_user_file', 'plant_calendar.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(calendar, f)

    my_thread = threading.Thread(target=simple_add_new_plant_, args=(
        id, name, represent_color, avatar, age, date_added, location, extra_notes, result, schedule))
    my_thread.start()
def simple_add_new_plant_(id,name,represent_color,avatar,age,date_added,location,extra_notes,result,schedule):
    basic = retrieve_plant_list()
    advanced = retrieve_plant_list_advanced()
    calendar = retrieve_plant_calendar()

    if basic is None:
        basic = dict()
        advanced = dict()
        calendar = dict()

    if id not in basic or basic[id] is None:
        basic[id] = dict()
        advanced[id] = dict()
        calendar[id] = dict()

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
    calendar[id][new_plant] = schedule

    with open(resources.path('placeholder_server.user', 'plant_selector.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(basic, f)
    with open(resources.path('placeholder_server.user', 'plant_selector_advanced.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(advanced, f)
    with open(resources.path('placeholder_server.user', 'plant_calendar.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(calendar, f)
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
                    else:
                        continue
    return calendar

# New user create with empty info------------------------------------------------------------------------
def update_plant_after_signup(id):
    # after sign up, the new user id is created, which is not yet in plant_selection list
    # so we create a relation by adding that new id

    basic = dict()
    advanced = dict()
    calendar = dict()
    cycle = dict()
    calendar_full = dict()

    with open(resources.path('app_config.local_user_file', 'plant_selector.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(basic, f)
    with open(resources.path('app_config.local_user_file', 'plant_selector_advanced.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(advanced, f)
    with open(resources.path('app_config.local_user_file', 'plant_calendar.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(calendar, f)
    with open(resources.path('app_config.local_user_file', 'cycle.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(cycle, f)
    with open(resources.path('app_config.local_user_file', 'calendar_full.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(calendar_full, f)

    # make api call
    my_thread = threading.Thread(target=update_plant_after_signup_, args=(id,))
    my_thread.start()
def update_plant_after_signup_(id):
    # after sign up, the new user id is created, which is not yet in plant_selection list
    # so we create a relation by adding that new id
    # make api call
    basic = retrieve_plant_list()
    advanced = retrieve_plant_list_advanced()
    calendar = retrieve_plant_calendar()
    cycle = retrieve_cycle()
    calendar_full = retrieve_calendar_full()

    if basic is None:
        basic = dict()
        advanced = dict()
        calendar = dict()
        cycle = dict()
        calendar_full = dict()

    basic[id] = dict()
    advanced[id] = dict()
    calendar[id] = dict()
    cycle[id] = dict()
    calendar_full[id] = dict()

    with open(resources.path('placeholder_server.user', 'plant_selector.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(basic, f)
    with open(resources.path('placeholder_server.user', 'plant_selector_advanced.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(advanced, f)
    with open(resources.path('placeholder_server.user', 'plant_calendar.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(calendar, f)
    with open(resources.path('placeholder_server.user', 'cycle.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(cycle,f)
    with open(resources.path('placeholder_server.user', 'calendar_full.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(calendar_full,f)

# Edit plant's calendar---------------------------------------------------------------------------------------
def simple_edit_plant_schedule(user_id, plant_id, schedule):
    calendar = get_plant_calendar()
    calendar[plant_id] = clean_calendar(schedule)

    with open(resources.path('app_config.local_user_file', 'plant_calendar.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(calendar, f)

    # make api call
    my_thread = threading.Thread(target=simple_edit_plant_schedule_, args=(user_id,plant_id,schedule))
    my_thread.start()

def simple_edit_plant_schedule_(user_id, plant_id, schedule):
    # api call to update schedule
    calendar = retrieve_plant_calendar()
    calendar[user_id][plant_id] = schedule

    with open(resources.path('placeholder_server.user', 'plant_calendar.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(calendar, f)

# api call to retrieve info
def retrieve_plant_list():
    plant_list = yaml.safe_load(open(resources.path('placeholder_server.user', 'plant_selector.yaml'), encoding='utf-8'))
    return plant_list
def retrieve_plant_list_advanced():
    plant_list_advanced = yaml.safe_load(open(resources.path('placeholder_server.user', 'plant_selector_advanced.yaml'), encoding='utf-8'))
    return plant_list_advanced
def retrieve_plant_calendar():
    plant_calendar = yaml.safe_load(open(resources.path('placeholder_server.user', 'plant_calendar.yaml'), encoding='utf-8'))
    return plant_calendar

def update_current_user(id):
    # make api call to retrieve user info
    plant_list = retrieve_plant_list()
    plant_list_advanced = retrieve_plant_list_advanced()
    plant_calendar = retrieve_plant_calendar()
    cycle = retrieve_cycle()
    calendar_full = retrieve_calendar_full()

    # update local file
    meta_config = yaml.safe_load(open(resources.path('app_config', 'meta_config.yaml'), encoding='utf-8'))
    meta_config['id'] = id

    with open(resources.path('app_config', 'meta_config.yaml'), 'w' ,encoding='utf-8') as f:
        yaml.safe_dump(meta_config, f)
    with open(resources.path('app_config.local_user_file', 'plant_selector.yaml'), 'w' ,encoding='utf-8') as f:
        yaml.safe_dump(plant_list[id], f)
    with open(resources.path('app_config.local_user_file', 'plant_selector_advanced.yaml'), 'w' ,encoding='utf-8') as f:
        yaml.safe_dump(plant_list_advanced[id], f)
    with open(resources.path('app_config.local_user_file', 'plant_calendar.yaml'), 'w' ,encoding='utf-8') as f:
        yaml.safe_dump(plant_calendar[id], f)
    with open(resources.path('app_config.local_user_file', 'cycle.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(cycle[id],f)
    with open(resources.path('app_config.local_user_file', 'calendar_full.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(calendar_full[id],f)

# load file from local
def get_plant_list():
    plant_list = yaml.safe_load(open(resources.path('app_config.local_user_file', 'plant_selector.yaml'), encoding='utf-8'))
    return plant_list
def get_plant_list_advanced():
    plant_list_advanced = yaml.safe_load(open(resources.path('app_config.local_user_file', 'plant_selector_advanced.yaml'), encoding='utf-8'))
    return plant_list_advanced
def get_plant_calendar():
    plant_calendar = yaml.safe_load(open(resources.path('app_config.local_user_file', 'plant_calendar.yaml'), encoding='utf-8'))
    return plant_calendar
