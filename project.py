# models/project.py
class Project:
    def __init__(self, title, details, total_target, start_time, end_time, owner_email):
        self.title = title
        self.details = details
        self.total_target = total_target
        self.start_time = start_time
        self.end_time = end_time
        self.owner_email = owner_email

    def __str__(self):
        return (f"Title: {self.title}\nDetails: {self.details}\nTarget: {self.total_target} EGP\n"
                f"Start Date: {self.start_time}\nEnd Date: {self.end_time}\nOwner: {self.owner_email}")