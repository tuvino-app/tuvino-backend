import uuid
from fastapi import HTTPException
import logging

from src.repository.base import BaseRepository, Session

class WinesRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    _table_name = "wines"

    def get_wine_preference_options(self):
        result = self.session.table(self._table_name) \
            .select("tipo, cuerpo") \
            .execute()

        return {
            'tipos': {item['tipo'] for item in result.data},
            'cuerpo': {item['cuerpo'] for item in result.data}

        }