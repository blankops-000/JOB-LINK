class User:
    def __init__(self, user_id, username, email):
        self.id = user_id
        self.username = username
        self.email = email

    def create(self):
        # Logic to create a new user in the database
        pass

    def update(self, username=None, email=None):
        # Logic to update user information
        if username:
            self.username = username
        if email:
            self.email = email
        pass

    def delete(self):
        # Logic to delete the user from the database
        pass

    @classmethod
    def find_by_id(cls, user_id):
        # Logic to find a user by their ID
        pass

    @classmethod
    def find_by_username(cls, username):
        # Logic to find a user by their username
        pass