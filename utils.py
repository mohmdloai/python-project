import re
from datetime import datetime

def validate_egyptian_phone(number):

    return re.match(r"^01[0125][0-9]{8}$", number) is not None

def validate_email(email):

    return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email) is not None

def validate_password(password):

    return len(password) >= 8

def validate_date(date_str):

    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False
def is_owner(project, user_email):

    return project.owner_email == user_email

def is_logged_in(project, user_email):

    return project.logged_in_email == user_email
#this func should be implemented !
#def is_unique_email(email):
