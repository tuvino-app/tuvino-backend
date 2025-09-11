from sqlalchemy import select
from typing import Optional, List
from src.repository.base import BaseRepository, Session
from src.models.wine import Wine

class WineRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def get_wine_by_id(self, wine_id: int) -> Optional[Wine]:
        response = self.supabase.table('wines').select('*').eq('wine_id', wine_id).execute()
        if response.data and len(response.data) > 0:
            return Wine(**response.data[0])
        return None

    def search_wines_by_name(self, name: str) -> List[Wine]:
        response = self.supabase.table('wines').select('*').ilike('wine_name', f'%{name}%').execute()
        return [Wine(**wine_data) for wine_data in response.data]