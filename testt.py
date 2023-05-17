try:
    from importlib import resources
except ImportError:
    import importlib_resources as resources
import yaml
import subprocess

a = yaml.safe_load(open('placeholder_server/user/user.yaml','r'))
username = 'a'
email = 'a@gmail.com'
password = 'a123'
new_user = {
    "user"+str(len(a)):
        {
            'username': username,
            'email': email,
            'password': password
        }
}

a.append(new_user)