import uuid

class User:
    uid: uuid.UUID
    username: str
    email: str

    def __init__(self, uid: uuid.UUID, username: str, email: str):
        self.uid = uid
        self.username = username
        self.email = email

    def uid_to_str(self):
        return str(self.uid)