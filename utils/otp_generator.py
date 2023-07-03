# generate otp for testing, will be replaced with api call
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
