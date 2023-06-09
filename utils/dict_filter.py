
def filter_dict_by_column(data_dict, column, filtering_key):
    filtered_dict = {}
    for key, value in data_dict.items():
        if column in value and filtering_key.lower() in value[column].lower():
            filtered_dict[key] = value
    return filtered_dict

def filter_calendar_full_by_plantid(calendar_full, id):
    filtered_dict = {}
    for week_range, days in calendar_full.items():
        filtered_dict[week_range] = dict()
        for day, hours_tasks in days.items():
            filtered_dict[week_range][day] = dict()
            for hour,tasks in hours_tasks.items():
                filtered_dict[week_range][day][hour] = []
                for task in tasks:
                    if task['callable_id'] == id:
                        filtered_dict[week_range][day][hour].append(task)
    return filtered_dict

def sort_dict_by_column(data_dict, column, reverse=False):
    if isinstance(next(iter(data_dict.values()))[column], str):  # Check if the column value is a string
        sorted_data = sorted(data_dict.items(), key=lambda item: item[1][column].lower(), reverse=reverse)
    else:
        sorted_data = sorted(data_dict.items(), key=lambda item: item[1][column], reverse=reverse)
    return dict(sorted_data)

the_dict = {
    'a': {
        'name': 'Fiddle a',
        'age': '2022/02'
    },
    'b': {
        'name': 'B',
        'age': '2012/08'
    },
    'c': {
        'name': 'centuck sa',
        'age': '2012/08'
    }
}

#print(sort_dict_by_column(the_dict,'name'))
