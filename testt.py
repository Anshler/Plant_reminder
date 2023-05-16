try:
    from importlib import resources
except ImportError:
    import importlib_resources as resources
import yaml
import subprocess
def get_otp():
    # Call the OTP program as a separate process
    subprocess.Popen("python "+str(resources.path('utils','otp_generator.py')))


def simple_otp_validation(text = '123456'):
    otp = open(resources.path('placeholder_server','otp.txt')).read()
    print(otp)

get_otp()
import time
time.sleep(2)
simple_otp_validation()