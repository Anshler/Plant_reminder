# set configuration e.g: theme
import yaml
from utils.android_port import get_file_path

meta_config = yaml.safe_load(open(get_file_path('app_config/meta_config.yaml'),encoding='utf-8'))
theme_list = yaml.safe_load(open(get_file_path('app_config/theme.yaml'),encoding='utf-8'))

theme = meta_config['theme']
language = meta_config['language']
volume = meta_config['volume']
current_user = meta_config['id']
alarm_ringtone = meta_config['alarm_ringtone']
background_image = meta_config['background_image']
def save_new_config(theme,language,volume):
    meta_config['theme'] = theme
    meta_config['language'] = language
    meta_config['volume'] = volume
    with open(get_file_path('app_config/meta_config.yaml'),'w',encoding='utf-8') as f:
        yaml.dump(meta_config,f)
