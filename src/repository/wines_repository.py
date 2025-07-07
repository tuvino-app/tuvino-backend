import uuid
from fastapi import HTTPException
import logging

from src.repository.base import SupabaseRepository

class WinesRepository(SupabaseRepository):
    _table_name = "vinos"

    def get_wine_preference_options(self):
        result = self.session.table(self._table_name) \
            .select("tipo, cuerpo") \
            .execute()

        return {
            'tipos': {item['tipo'] for item in result.data},
            'cuerpo': {item['cuerpo'] for item in result.data}

        }