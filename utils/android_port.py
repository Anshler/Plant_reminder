from kivy.utils import platform
import os
try:
    from importlib import resources
except ImportError:
    import importlib_resources as resources

def get_file_path(file:str):
    if platform == 'android':
        import android
        return os.path.join(android.storage.app_storage_path(), file)
    else:
        file = file.split('/')
        if len(file) == 1:
            return resources.path('', file[0])
        else:
            return resources.path('.'.join(file[:-1]), file[-1])
