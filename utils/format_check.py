import re

# Password must be atleast 8 characters long, contain numbers, special and capital letters
# username and email must have at least 1 word letter
def isPasswordFormat(password, *args) -> bool:
    # Check length
    if len(password) < 8:
        return False

    # Check for symbols
    #if not re.search(r"[!@#$%^&*()\-_=+{};:,<.>]", password):
        #return False

    # Check for capital letters
    if not re.search(r"[A-Z]", password):
        return False

    # Check for non-capital letters
    if not re.search(r"[a-z]", password):
        return False

    # Check for numbers
    if not re.search(r"[0-9]", password):
        return False
    return True

def isUsernameFormat(username, *args) -> bool:
    # Check length
    if len(username) < 1:
        return False
    # Check for capital letters
    if not re.search(r"[A-Z]", username) and not re.search(r"[a-z]", username):
        return False
    return True
