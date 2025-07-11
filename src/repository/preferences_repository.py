import logging

from sqlalchemy import select

from src.repository.base import BaseRepository, Session
from src.models.preference import Preference
from src.models.preference_category import PreferenceCategory
from src.repository.table_models.preference_options import PreferenceOption as PreferenceOptionModel
from src.repository.table_models.preference_categories import PreferenceCategory as PreferenceCategoryModel

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
            preference = Preference(option.id, option.option, option.description)
            preference.set_category(category)
            results.append(preference)
        return results