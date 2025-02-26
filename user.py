# models/user.py
class User:
    def __init__(self, first_name, last_name, email, password, mobile_phone):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.mobile_phone = mobile_phone

    def __str__(self):
        return f"User: {self.first_name} {self.last_name}, Email: {self.email}"