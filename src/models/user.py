import uuid
import logging
from src.models.preference import Preference
from src.models.rating import Rating
from src.models.wine import Wine

class User:
    uid: uuid.UUID
    username: str
    email: str
    onboarding_completed: bool
    preferences: list
    favorites: list

    def __init__(self, uid: uuid.UUID, username: str, email: str):
        self.uid = uid
        self.username = username
        self.email = email
        self.preferences = []

    def uid_to_str(self):
        return str(self.uid)

    def add_preferences(self, preferences):
        if not preferences:
            raise ValueError("El usuario no tiene preferencias registradas")
        self.preferences = preferences
        self.onboarding_completed = True

    def favorite_type(self):
        types = {'Tinto': 'Red', 'Blanco': 'White', 'Rosado': 'Rose', 'Espumoso': 'Sparkling'}
        for preference in self.preferences:
            if preference.category.category == 'types':
                return types[preference.option]
        return None

    def favorite_body(self):
        return 1

    def favorite_dryness(self):
        return 1

    def favorite_abv(self):
        return 11

    def rate_wine(self, wine_id, rating):
        return Rating(self.uid, wine_id, rating)

    def add_favorite(self, wine: Wine):
        self.favorites.append(wine)

    def set_favorites(self, favorites: list):
        self.favorites = favorites

    def get_favorites(self):
        return self.favorites