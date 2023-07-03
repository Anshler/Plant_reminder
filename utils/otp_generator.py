# generate otp for testing, will be replaced with api call

from kivy.utils import platform
from kivy.resources import resource_add_path
if platform == 'android':
    import android
    project_dir = android.PythonActivity.mActivity.getFilesDir().getAbsolutePath()
    resource_add_path(project_dir)
    from utils.android_port import get_file_path
else:
    from utils.android_port import get_file_path
import yaml
import random,time

# Generate random 6-digit number
otp = random.randint(100000, 999999)
# Save OTP to a text file
with open(get_file_path('placeholder_server/otp.txt'), 'w') as file:
    file.write(str(otp))
# Wait for 2 minutes
time.sleep(120)
# Override the file with an empty string
with open(get_file_path('placeholder_server/otp.txt'), 'w') as file:
    file.write('')
