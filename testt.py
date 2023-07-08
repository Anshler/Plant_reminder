import yaml
from utils.plant_profile_management import clean_calendar
a = yaml.safe_load(open('app_config/local_user_file/plant_calendar.yaml'))['281cd5f5-f100-4755-a153-be190848cea0']
print(a)
print(clean_calendar(a))
