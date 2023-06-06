# Check if user had login at least once in the past
# if not, open signup screen, else, open login screen
try:
    from importlib import resources
except ImportError:
    import importlib_resources as resources
import yaml

def ReadHadStartup() -> bool:
    historical_startup = yaml.safe_load(open(resources.path('app_config', 'had_startup.yaml'),'r'))
    status = historical_startup['had_startup']
    return status
def WriteHadStartUp() -> bool:
    historical_startup = yaml.safe_load(open(resources.path('app_config', 'had_startup.yaml'), 'r'))
    historical_startup['had_startup'] = True
    with open(resources.path('app_config', 'had_startup.yaml'), 'w') as f:
        yaml.dump(historical_startup,f)

def ReadHadLogin() -> bool:
    historical_login = yaml.safe_load(open(resources.path('app_config', 'had_startup.yaml'),'r'))
    status = historical_login['had_login']
    return status
def WriteHadLogin(status = True) -> bool:
    historical_login = yaml.safe_load(open(resources.path('app_config', 'had_startup.yaml'), 'r'))
    historical_login['had_login'] = status
    with open(resources.path('app_config', 'had_startup.yaml'), 'w') as f:
        yaml.dump(historical_login,f)
