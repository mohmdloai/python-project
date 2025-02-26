import json
import os
from user import User
from project import Project
from utils import *
# from utils import validate_email, validate_password, validate_egyptian_phone, validate_date, is_owner


class CrowdfundingApp:
    # # class variables to store data
    # only saved during working session
    users = []
    projects = []
    logged_in_user = None

    # JSON file paths to send and retrieve data
    # Instead of class vars to store data in json files usng " with open " from
    USERS_FILE = "users.json"
    PROJECTS_FILE = "projects.json"

    @classmethod
    def load_data(cls):
        """Load users and projects from JSON files."""
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)

        # Load users
        if os.path.exists(cls.USERS_FILE):
            with open(cls.USERS_FILE, "r") as file:
                users_data = json.load(file)
                cls.users = [User(**user) for user in users_data] #unpack for dics , listing the objs within list

        # Load projects
        if os.path.exists(cls.PROJECTS_FILE):
            with open(cls.PROJECTS_FILE, "r") as file:
                projects_data = json.load(file)
                cls.projects = [Project(**project) for project in projects_data]

    @classmethod
    def save_data(cls):
        """Save users and projects to JSON files."""
        # Save users
        with open(cls.USERS_FILE, "w") as file:
            users_data = [user.__dict__ for user in cls.users]
            json.dump(users_data, file, indent=4)

        # Save projects
        with open(cls.PROJECTS_FILE, "w") as file:
            projects_data = [project.__dict__ for project in cls.projects]
            json.dump(projects_data, file, indent=4)

    def __init__(self):
        # Load data when the app starts
        self.load_data()

    def register(self):
        print("\n--- Registration ---")
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        email = input("Email: ")
        while not validate_email(email):
            print("Invalid email format. Please try again.")
            email = input("Email: ")

        password = input("Password: ")
        while not validate_password(password):
            print("Password must be at least 8 characters long.")
            password = input("Password: ")

        confirm_password = input("Confirm Password: ")
        while password != confirm_password:
            print("Passwords do not match. Please try again.")
            confirm_password = input("Confirm Password: ")

        mobile_phone = input("Mobile Phone (Egyptian): ")
        while not validate_egyptian_phone(mobile_phone):
            print("Invalid Egyptian phone number. Please try again.")
            mobile_phone = input("Mobile Phone (Egyptian): ")

        user = User(first_name, last_name, email, password, mobile_phone)
        self.users.append(user)
        self.save_data()  # Save updated users to JSON
        print("Registration successful! You can now login.")

    def login(self):
        print("\n--- Login ---")
        email = input("Email: ")
        password = input("Password: ")

        for user in self.users:
            if user.email == email and user.password == password:
                self.logged_in_user = user
                print(f"Welcome back, {user.first_name}!")
                return
        print("Invalid email or password.")

    def create_project(self):
        if not self.logged_in_user:
            print("You must be logged in to create a project.")
            return

        print("\n--- Create Project ---")
        title = input("Title: ")
        details = input("Details: ")
        total_target = float(input("Total Target (EGP): "))

        start_time = input("Start Date (YYYY-MM-DD): ")
        while not validate_date(start_time):
            print("Invalid date format. Please use YYYY-MM-DD.")
            start_time = input("Start Date (YYYY-MM-DD): ")

        end_time = input("End Date (YYYY-MM-DD): ")
        while not validate_date(end_time) or end_time <= start_time:
            print("Invalid date. End date must be after start date.")
            end_time = input("End Date (YYYY-MM-DD): ")

        project = Project(title, details, total_target, start_time, end_time, self.logged_in_user.email)
        self.projects.append(project)
        self.save_data()  # Save updated projects to JSON
        print("Project created successfully!")

    def view_my_projects(self):
        """Allow the logged-in user to view only their own projects."""
        if not self.logged_in_user:
            print("You must be logged in to view your projects.")
            return

        print("\n--- My Projects ---")
        my_projects = [p for p in self.projects if is_owner(p, self.logged_in_user.email)]
        if not my_projects:
            print("You have no projects.")
        else:
            for project in my_projects:
                print(project)
                print("-" * 30)
    def edit_project(self):
        if not self.logged_in_user:
            print("You must be logged in to edit a project.")
            return

        print("\n--- Edit Project ---")
        title = input("Enter the title of the project you want to edit: ")

        for project in self.projects:
            if project.title == title and project.owner_email == self.logged_in_user.email:
                print("Leave blank to keep the current value.")
                new_title = input(f"New Title ({project.title}): ") or project.title
                new_details = input(f"New Details ({project.details}): ") or project.details
                new_target = input(f"New Target ({project.total_target} EGP): ") or project.total_target
                new_start = input(f"New Start Date ({project.start_time}): ") or project.start_time
                new_end = input(f"New End Date ({project.end_time}): ") or project.end_time

                project.title = new_title
                project.details = new_details
                project.total_target = float(new_target)
                project.start_time = new_start
                project.end_time = new_end
                self.save_data()  # Save updated projects to JSON
                print("Project updated successfully!")
                return
        print("Project not found or you do not have permission to edit it.")

    def delete_my_project(self):
        """Allow the logged-in user to delete only their own projects."""
        if not self.logged_in_user:
            print("You must be logged in to delete a project.")
            return

        print("\n--- Delete My Project ---")
        title = input("Enter the title of the project you want to delete: ")

        for project in self.projects:
            if project.title == title and is_owner(project, self.logged_in_user.email):
                self.projects.remove(project)
                self.save_data()  # Save updated projects to JSON
                print("Project deleted successfully!")
                return
        print("Project not found or you do not have permission to delete it.")

    def search_by_date(self):
        print("\n--- Search Projects by Date ---")
        date = input("Enter date (YYYY-MM-DD): ")
        if not self.logged_in_user:
            print("You must be logged in to create a project.")
            return
        # if not is_owner(self,user_email=self.logged_in_user.email):
        #     print("You must be logged in to search for projects.")
        #     return
        if not validate_date(date):
            print("Invalid date format.")
            return

        found_projects = [p for p in self.projects if p.start_time <= date <= p.end_time]
        if not found_projects:
            print("No projects found for the given date.")
        else:
            for project in found_projects:
                print(project)
                print("-" * 30)

    def main_menu(self):
        while True:
            print("\n--- Crowdfunding App ---")
            print("1. Register")
            print("2. Login")
            print("3. Create Project")
            print("4. View My Projects")
            print("5. Edit My Project")
            print("6. Delete My Project")
            print("7. Search Projects by Date")
            print("8. Exit")
            choice = input("Choose an option: ")

            if choice == "1":
                self.register()
            elif choice == "2":
                self.login()
            elif choice == "3":
                self.create_project()
            elif choice == "4":
                self.view_my_projects()
            elif choice == "5":
                self.edit_project()
            elif choice == "6":
                self.delete_my_project()
            elif choice == "7":
                self.search_by_date()
            elif choice == "8":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")