import logging
from typing import List, Dict, Optional

from src.utilities.supabase_client import supabase
from src.models.preference import Preference
from src.models.preference_category import PreferenceCategory


class PreferencesRepository:
    """Repository for preferences operations using Supabase"""

    def get_options(self) -> List[Preference]:
        """Get all available preference options with their categories"""
        response = supabase.table("preference_options")\
            .select("*, preference_categories(*)")\
            .execute()

        results = []
        if response.data:
            for option in response.data:
                preference = Preference(
                    option['id'],
                    option['option'],
                    option.get('description', ''),
                    option.get('value', 0.0)
                )
                category_data = option.get('preference_categories')
                if category_data:
                    preference.set_category(PreferenceCategory(
                        category_data['id'],
                        category_data['name'],
                        category_data.get('description', '')
                    ))
                results.append(preference)
        return results

    def get_preferences(self, user_id: str) -> List[Preference]:
        """Get user preferences"""
        try:
            response = supabase.table("user_preferences")\
                .select("*, preference_options(*, preference_categories(*))")\
                .eq("user_id", user_id)\
                .execute()

            user_preferences = []
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
                            pref.set_category(PreferenceCategory(
                                category_data['id'],
                                category_data['name'],
                                category_data.get('description', '')
                            ))
                        user_preferences.append(pref)

            return user_preferences

        except Exception as e:
            logging.error(f"Error al obtener preferencias: {str(e)}")
            return []

    def save_onboarding_preferences(
        self,
        user_id: str,
        preference_options: List[int],
        weights: Optional[Dict] = None
    ) -> bool:
        """
        Save all user preferences during onboarding

        Args:
            user_id: User UUID
            preference_options: List of preference option IDs
            weights: Optional dictionary of {option_id: weight} for custom weights
        """
        try:
            # Delete existing preferences for this user
            supabase.table("user_preferences")\
                .delete()\
                .eq("user_id", user_id)\
                .execute()

            # Verify option IDs exist
            valid_options_response = supabase.table("preference_options")\
                .select("id")\
                .execute()
            valid_options = set(opt['id'] for opt in valid_options_response.data) if valid_options_response.data else set()

            invalid_options = [opt_id for opt_id in preference_options if opt_id not in valid_options]
            if invalid_options:
                raise ValueError(f"Opciones de preferencia inválidas: {invalid_options}")

            # Add new preferences
            new_preferences = []
            for option_id in preference_options:
                weight = weights.get(option_id, 1.0) if weights else 1.0
                new_preferences.append({
                    "user_id": user_id,
                    "option_id": option_id,
                    "weight": weight
                })

            if new_preferences:
                supabase.table("user_preferences").insert(new_preferences).execute()

            return True

        except Exception as e:
            logging.error(f"Error saving preferences: {str(e)}")
            raise e

    def update_category_preferences(
        self,
        user_id: str,
        category_id: int,
        preference_options: List[int],
        weights: Optional[Dict] = None
    ) -> bool:
        """
        Update preferences for a specific category

        Args:
            user_id: User UUID
            category_id: Category ID to update
            preference_options: List of preference option IDs within that category
            weights: Optional dictionary of {option_id: weight} for custom weights
        """
        try:
            # Get all option IDs for this category
            category_options_response = supabase.table("preference_options")\
                .select("id")\
                .eq("category_id", category_id)\
                .execute()

            category_option_ids = [opt['id'] for opt in category_options_response.data] if category_options_response.data else []

            # Delete existing preferences for this category
            if category_option_ids:
                supabase.table("user_preferences")\
                    .delete()\
                    .eq("user_id", user_id)\
                    .in_("option_id", category_option_ids)\
                    .execute()

            # Add new preferences
            new_preferences = []
            for option_id in preference_options:
                if option_id in category_option_ids:
                    weight = weights.get(option_id, 1.0) if weights else 1.0
                    new_preferences.append({
                        "user_id": user_id,
                        "option_id": option_id,
                        "weight": weight
                    })

            if new_preferences:
                supabase.table("user_preferences").insert(new_preferences).execute()

            return True

        except Exception as e:
            logging.error(f"Error updating category preferences: {str(e)}")
            raise e

    def get_user_preference_attributes(self, user_id: str) -> Dict:
        """
        Get user preferences grouped by categories for ML model
        """
        result = {
            "types": {},
            "bodies": {},
            "intensities": {},
            "dryness": {},
            "abv": {}
        }

        try:
            preferences = self.get_preferences(user_id)

            if not preferences:
                return result

            # Category name mapping
            category_name_map = {
                "types": "types",
                "bodies": "bodies",
                "intensities": "intensities",
                "dryness": "dryness",
                "abv": "abv"
            }

            # Group preferences by category
            for pref in preferences:
                if hasattr(pref, 'category') and pref.category:
                    category_name = pref.category.name.lower()
                    if category_name in category_name_map:
                        key = category_name_map[category_name]
                        result[key][pref.id] = float(pref.value)

            return result

        except Exception as e:
            logging.error(f"Error al obtener preferencias de usuario: {str(e)}")
            return result
