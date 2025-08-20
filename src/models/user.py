import uuid
from src.models.preference import Preference

class User:
    uid: uuid.UUID
    username: str
    email: str
    onboarding_completed: bool
    preferences: list

    def __init__(self, uid: uuid.UUID, username: str, email: str):
        self.uid = uid
        self.username = username
        self.email = email
        self.preferences = []

    def uid_to_str(self):
        return str(self.uid)

    def add_preferences(self, preferences):
        for category, preference_id in preferences:
            prefence = Preference(preference_id, '', '')
            self.preferences.append(prefence)
        self.onboarding_completed = True