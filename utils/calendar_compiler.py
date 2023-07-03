import datetime
import yaml
import numpy as np
import threading
from utils.android_port import get_file_path

def update_calendar(id):
    # cycle is the first monday to final sunday when the previous calendar was first created.
    cycle = get_cycle()
    task_list = yaml.safe_load(open(get_file_path('app_config/local_user_file/plant_calendar.yaml'), encoding='utf-8'))
    plant_list = yaml.safe_load(open(get_file_path('app_config/local_user_file/plant_selector.yaml'), encoding='utf-8'))
    # number of weeks is smallest common multiple of all the task frequency
    frequencies = []
    for plant in task_list.values():
        if plant is None:
            continue
        for day in plant.values():
            for item in day:
                frequencies.append(item['frequency'])
    weeks = int(np.lcm.reduce(frequencies)) if len(frequencies) != 0 else 0
    # Update calendar
    # Get last Monday's date
    today = datetime.date.today()
    last_monday = today - datetime.timedelta(days=today.weekday())

    if cycle is not None and cycle != {}:
        start_cycle = cycle['start_cycle']
        end_cycle = cycle['end_cycle']

        # update to new cycle
        if start_cycle <= last_monday < end_cycle:
            last_monday = start_cycle
            while weeks != 0:
                if last_monday + datetime.timedelta(weeks=weeks) < end_cycle and last_monday + datetime.timedelta(weeks=weeks) <= datetime.date.today():
                    last_monday += datetime.timedelta(weeks=weeks)
                else: break
    else:
        cycle = dict()
    start_cycle = last_monday # new first monday
    end_cycle = last_monday + datetime.timedelta(weeks=weeks) - datetime.timedelta(days=1) # new final sunday
    cycle['start_cycle'] = start_cycle
    cycle['end_cycle'] = end_cycle

    # open calendar_full file
    # will be done later
    data = {}

    for i in range(weeks):
        week_start = last_monday + datetime.timedelta(weeks=i)
        week_end = week_start + datetime.timedelta(days=6)
        week_key = f"{week_start.strftime('%Y-%m-%d')}_{week_end.strftime('%Y-%m-%d')}"

        week_data = {}
        for j in range(7):
            day = week_start + datetime.timedelta(days=j)
            day_key = day.strftime('%A').lower()
            week_data[day_key] = dict()

        data[week_key] = week_data

    calendar_full = add_task_to_calendar(data, task_list, plant_list)

    with open(get_file_path('app_config/local_user_file/cycle.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(cycle,f)
    with open(get_file_path('app_config/local_user_file/calendar_full.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(calendar_full,f)

    # make api call
    my_thread = threading.Thread(target=update_calendar_, args=(id,cycle,calendar_full))
    my_thread.start()
def update_calendar_(id,current_cycle, current_calendar_full):
    cycle = retrieve_cycle()
    calendar_full = retrieve_calendar_full()

    cycle[id] = current_cycle
    calendar_full[id] = current_calendar_full
    # this will be an api call in the future
    with open(get_file_path('placeholder_server/user/cycle.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(cycle,f)
    with open(get_file_path('placeholder_server/user/calendar_full.yaml'), 'w', encoding='utf-8') as f:
        yaml.safe_dump(calendar_full,f)

def add_task_to_calendar(calendar, task_list, plant_list):
    num_weeks = len(calendar)
    keys = list(calendar.keys())
    for plant in task_list:
        if task_list[plant] is None:
            continue
        represent_color = plant_list[plant]['represent_color']
        name = plant_list[plant]['name']
        for day, tasks in task_list[plant].items():
            for task in tasks:
                frequency = task['frequency']
                hour = task['hour']
                task_name = task['task']

                # Skip the desired number of keys using islice
                for i in range(0,len(keys),frequency):
                    if hour not in calendar[keys[i]][day]:
                        calendar[keys[i]][day][hour] = []
                    calendar[keys[i]][day][hour].append({'callable_id': plant, 'name': name,'represent_color': represent_color,'task': task_name, 'frequency': str(frequency)})
    return calendar

def get_cycle():
    cycle = yaml.safe_load(open(get_file_path('app_config/local_user_file/cycle.yaml'), encoding='utf-8'))
    return cycle
def get_calendar_full():
    calendar_full = yaml.safe_load(open(get_file_path('app_config/local_user_file/calendar_full.yaml'), encoding='utf-8'))
    return calendar_full

def retrieve_cycle():
    cycle = yaml.safe_load(open(get_file_path('placeholder_server/user/cycle.yaml'), encoding='utf-8'))
    return cycle
def retrieve_calendar_full():
    calendar_full = yaml.safe_load(open(get_file_path('placeholder_server/user/calendar_full.yaml'), encoding='utf-8'))
    return calendar_full

def get_current_week_range():
    today = datetime.date.today()
    last_monday = today - datetime.timedelta(days=today.weekday())
    current_week_range = str(last_monday) + '_' + str(last_monday + datetime.timedelta(days=6))
    return current_week_range
