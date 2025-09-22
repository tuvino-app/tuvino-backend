import logging

from sqlalchemy import select

from src.repository.base import BaseRepository, Session
from src.models.preference import Preference
from src.models.preference_category import PreferenceCategory
from src.repository.table_models.preference_options import PreferenceOption as PreferenceOptionModel
from src.repository.table_models.preference_categories import PreferenceCategory as PreferenceCategoryModel
from src.repository.table_models.user_preferences import UserPreference as UserPreferenceModel

class PreferencesRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def get_options(self):
        query = select(PreferenceCategoryModel, PreferenceOptionModel).join(
            PreferenceOptionModel,
            PreferenceCategoryModel.id == PreferenceOptionModel.category_id
        )

        results = []
        for category, option in self.session.execute(query):
            preference = Preference(option.id, option.option, option.description, option.value)
            preference.set_category(category)
            results.append(preference)
        return results

    def get_preferences(self, user_id):
        preferences = (self.session.query(
            UserPreferenceModel,
            PreferenceOptionModel,
            PreferenceCategoryModel,
        ).join(
            PreferenceOptionModel,
            UserPreferenceModel.option_id == PreferenceOptionModel.id
        )
        .join(
            PreferenceCategoryModel,
            PreferenceCategoryModel.id == PreferenceOptionModel.category_id,
        )
        .filter(
            UserPreferenceModel.user_id == user_id
        ).all())
        user_preferences = []
        for (user_pref, option, category) in preferences:
            pref = Preference(
                option.id,
                option.option,
                option.description,
                option.value
            )
            pref.set_category(PreferenceCategory(category.id, category.name, category.description))
            user_preferences.append(pref)
        return user_preferences