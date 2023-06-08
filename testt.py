import datetime
import yaml
try:
    from importlib import resources
except ImportError:
    import importlib_resources as resources

calendar = yaml.safe_load(open(resources.path('app_config.local_user_file', 'calendar_full.yaml'), encoding='utf-8'))

closest_event, closest_date_range, closest_day, closest_time, closest_time_distance = get_next_event(calendar)

print(closest_event)
print(closest_date_range)
print(closest_day)
print(closest_time)
print(closest_time_distance)
