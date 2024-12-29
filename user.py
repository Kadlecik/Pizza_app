# user.py
class User:
    def __init__(self, username, password, role="user"):
        self.username = username
        self.password = password  # Pozor, hesla by měla být vždy hashována
        self.role = role  # Role uživatele, například "admin" nebo "user"

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "role": self.role
        }

    @staticmethod
    def from_dict(data):
        return User(data['username'], data['password'], data['role'])
