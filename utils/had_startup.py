# Check if user had login at least once in the past
# if not, open signup screen, else, open login screen
import yaml
from kivy.utils import platform
from kivy.resources import resource_add_path
if platform == 'android':
    import android
    project_dir = android.PythonActivity.mActivity.getFilesDir().getAbsolutePath()
    resource_add_path(project_dir)
    from utils.android_port import get_file_path
else:
    from utils.android_port import get_file_path
def ReadHadStartup() -> bool:
    historical_startup = yaml.safe_load(open(get_file_path('app_config/had_startup.yaml'),'r'))
    status = historical_startup['had_startup']
    return status
def WriteHadStartUp() -> bool:
    historical_startup = yaml.safe_load(open(get_file_path('app_config/had_startup.yaml'), 'r'))
    historical_startup['had_startup'] = True
    with open(get_file_path('app_config/had_startup.yaml'), 'w') as f:
        yaml.dump(historical_startup,f)

def ReadHadLogin() -> bool:
    historical_login = yaml.safe_load(open(get_file_path('app_config/had_startup.yaml'),'r'))
    status = historical_login['had_login']
    return status
def WriteHadLogin(status = True) -> bool:
    historical_login = yaml.safe_load(open(get_file_path('app_config/had_startup.yaml'), 'r'))
    historical_login['had_login'] = status
    with open(get_file_path('app_config/had_startup.yaml'), 'w') as f:
        yaml.dump(historical_login,f)
