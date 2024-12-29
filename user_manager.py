import json
from user import User

class UserManager:
    def __init__(self, users_file="users.json"):
        self.users_file = users_file
        self.users = self.load_users()

    def load_users(self):
        try:
            with open(self.users_file, 'r') as file:
                users_data = json.load(file)
                return [User.from_dict(user_data) for user_data in users_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_users(self):
        with open(self.users_file, 'w') as file:
            json.dump([user.to_dict() for user in self.users], file)

    def add_user(self, username, password, role="user"):
        new_user = User(username, password, role)
        self.users.append(new_user)
        self.save_users()

    def edit_user(self, username, new_password=None, new_role=None):
        for user in self.users:
            if user.username == username:
                if new_password:
                    user.password = new_password
                if new_role:
                    user.role = new_role
                self.save_users()
                return True
        return False

    def delete_user(self, username):
        self.users = [user for user in self.users if user.username != username]
        self.save_users()

    def validate_user(self, username, password):
        print(f"Validating user: {username}, with password: {password}")  # Ladicí výstup
        for user in self.users:
            print(f"Checking user: {user.username}, with stored password: {user.password}")  # Ladicí výstup
            if user.username == username and user.password == password:
                print("Login successful!")  # Ladicí výstup
                return True
        print("Login failed!")  # Ladicí výstup
        return False
