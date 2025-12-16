import uuid
import logging
from typing import List

from src.utilities.supabase_client import supabase
from src.models.wine import Wine
from src.models.user import User
from src.models.preference import Preference
from src.models.rating import Rating

class UsersRepository:
    """Repository for user operations using Supabase"""

    def get_user_by_id(self, user_uid: str) -> User:
        """Get user by UUID from Supabase"""
        try:
            uuid.UUID(user_uid)
        except ValueError:
            logging.error(f'El id {user_uid} no es un UUID valido')
            raise KeyError('Formato de ID de usuario invalido')

        # Get user from Supabase
        response = supabase.table("users").select("*").eq("uid", user_uid).execute()

        if not response.data or len(response.data) == 0:
            raise KeyError('El usuario no existe')

        user_data = response.data[0]
        user = User(
            uid=uuid.UUID(user_data['uid']),
            username=user_data.get('name', ''),
            email=user_data.get('email', '')
        )
        user.onboarding_completed = user_data.get('onboarding_completed', False)

        # Load preferences
        try:
            user.add_preferences(self._get_user_preferences(user.uid_to_str()))
        except Exception as e:
            logging.warning(f"Could not load preferences for user {user_uid}: {e}")
            user.preferences = []

        # Load favorites
        user.set_favorites(self.get_favorite_wines(user))

        # Load ratings
        user.set_ratings(self._get_user_ratings(user.uid_to_str()))

        return user

    def get_favorite_wines(self, user: User) -> List[Wine]:
        """Get user's favorite wines from Supabase"""
        # Get favorite wine IDs
        fav_response = supabase.table("favorite_wines")\
            .select("wine_id")\
            .eq("user_id", user.uid_to_str())\
            .order("added_date", desc=True)\
            .execute()

        wines = []
        if fav_response.data:
            wine_ids = [fav['wine_id'] for fav in fav_response.data]

            # Fetch wine details for these IDs
            if wine_ids:
                wines_response = supabase.table("wines")\
                    .select("*")\
                    .in_("wine_id", wine_ids)\
                    .execute()

                if wines_response.data:
                    # Create a mapping to preserve order
                    wines_map = {w['wine_id']: w for w in wines_response.data}

                    for wine_id in wine_ids:
                        wine_data = wines_map.get(wine_id)
                        if wine_data:
                            wines.append(Wine(
                                wine_data['wine_id'],
                                wine_data['wine_name'],
                                wine_data['type'],
                                wine_data['elaborate'],
                                wine_data['abv'],
                                wine_data['body'],
                                wine_data['country'],
                                wine_data['region'],
                                wine_data['winery'],
                                wine_data.get('summary')
                            ))
        return wines

    def _get_user_preferences(self, user_id: str) -> List[Preference]:
        """Get user preferences from Supabase"""
        # Join user_preferences with preference_options and preference_categories
        response = supabase.table("user_preferences")\
            .select("*, preference_options(*, preference_categories(*))")\
            .eq("user_id", user_id)\
            .execute()

        preferences = []
        if response.data:
            for up in response.data:
                option = up.get('preference_options')
                if option:
                    pref = Preference(
                        option['id'],
                        option['option'],
                        option.get('description', ''),
                        option.get('value', 0.0)
                    )
                    category_data = option.get('preference_categories')
                    if category_data:
                        from src.models.preference_category import PreferenceCategory
                        pref.set_category(PreferenceCategory(
                            category_data['id'],
                            category_data['name'],
                            category_data.get('description', '')
                        ))
                    preferences.append(pref)
        return preferences

    def _get_user_ratings(self, user_id: str) -> List[Rating]:
        """Get user ratings from Supabase"""
        # Get user ratings
        response = supabase.table("wine_ratings")\
            .select("*")\
            .eq("user_id", user_id)\
            .order("date", desc=True)\
            .execute()

        ratings = []
        if response.data:
            # Get unique wine IDs from ratings
            wine_ids = list(set(r['wine_id'] for r in response.data))

            # Fetch wine details
            wines_map = {}
            if wine_ids:
                wines_response = supabase.table("wines")\
                    .select("*")\
                    .in_("wine_id", wine_ids)\
                    .execute()

                if wines_response.data:
                    wines_map = {w['wine_id']: w for w in wines_response.data}

            # Build ratings with wine data
            for rating_data in response.data:
                wine_data = wines_map.get(rating_data['wine_id'])
                if wine_data:
                    wine = Wine(
                        wine_data['wine_id'],
                        wine_data['wine_name'],
                        wine_data['type'],
                        wine_data['elaborate'],
                        wine_data['abv'],
                        wine_data['body'],
                        wine_data['country'],
                        wine_data['region'],
                        wine_data['winery'],
                        wine_data.get('summary')
                    )
                    ratings.append(Rating(
                        rating_data['user_id'],
                        wine,
                        rating_data.get('rating'),
                        rating_data.get('review')
                    ))
        return ratings

    def save(self, user: User):
        """Save or update user in Supabase"""
        logging.info(f'Saving user with ID {user.uid_to_str()}')

        # Check if user exists
        existing = supabase.table("users").select("uid").eq("uid", user.uid_to_str()).execute()

        user_data = {
            "uid": user.uid_to_str(),
            "name": user.username,
            "email": user.email
        }

        if existing.data and len(existing.data) > 0:
            # Update existing user
            supabase.table("users").update(user_data).eq("uid", user.uid_to_str()).execute()
        else:
            # Insert new user
            supabase.table("users").insert(user_data).execute()

        # Save preferences
        current_prefs = self._get_user_preferences(user.uid_to_str())
        current_pref_ids = [p.id for p in current_prefs]

        for preference in user.preferences:
            preference_id = preference if isinstance(preference, int) else preference.id
            if preference_id not in current_pref_ids:
                logging.info(f'New preference detected: {preference_id} saving...')
                supabase.table("user_preferences").insert({
                    "user_id": user.uid_to_str(),
                    "option_id": preference_id
                }).execute()
                # Mark onboarding as complete
                supabase.table("users").update({
                    "onboarding_completed": True
                }).eq("uid", user.uid_to_str()).execute()

        # Save favorites
        current_favorites = self.get_favorite_wines(user)
        current_favorite_ids = [fav.id for fav in current_favorites]

        for favorite in user.get_favorites():
            if favorite.id not in current_favorite_ids:
                logging.info(f'New favorite detected: {favorite.wine_id} saving...')
                supabase.table("favorite_wines").insert({
                    "user_id": user.uid_to_str(),
                    "wine_id": favorite.wine_id
                }).execute()

        return user

    def delete_favorite_wine(self, user: User, wine_id: int):
        """Remove a wine from user's favorites"""
        favorite_ids = [fav.id for fav in user.get_favorites()]
        if wine_id not in favorite_ids:
            raise ValueError('Wine not in favorites')

        supabase.table("favorite_wines")\
            .delete()\
            .eq("user_id", user.uid_to_str())\
            .eq("wine_id", wine_id)\
            .execute()
