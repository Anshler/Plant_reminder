'''import os
from kivy.utils import platform
from kivy.resources import resource_find
if platform == 'android':
    from android.storage import app_storage_path
    from android import mActivity
else:
    try:
        from importlib import resources
    except ImportError:
        import importlib_resources as resources
def get_external_file_path(file:str):
    if platform == 'android':
        context = mActivity.getApplicationContext()
        result = context.getExternalFilesDir(None)  # don't forget the argument
        if result:
            storage_path = str(result.toString())
        else:
            storage_path = app_storage_path()
        return os.path.join(storage_path, file)
    else:
        file = file.split('/')
        if len(file) == 1:
            return resources.path('', file[0])
        else:
            return resources.path('.'.join(file[:-1]), file[-1])'''
def get_file_path(file:str):
    return file
