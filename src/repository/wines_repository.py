from src.utilities.supabase_client import supabase
from src.models.schemas.wines import WineSchema
import uuid

class WinesRepository:
    table_name = "wines"

    @staticmethod
    def get_by_id(wine_id: int):
        response = supabase.table(WinesRepository.table_name).select("*").eq("wine_id", wine_id).single().execute()
        if not getattr(response, "data", None):
            return None
        return WineSchema(**response.data)

    @staticmethod
    def get_by_name(wine_name: str):
        # Búsqueda parcial: contiene la cadena (insensible a mayúsculas/minúsculas)
        response = supabase.table(WinesRepository.table_name).select("*").ilike("wine_name", "%" + wine_name + "%").execute()
        if not getattr(response, "data", None):
            return []
        
        # Ordenar: primero los que empiecen con la cadena, luego los que la contengan
        wines = [WineSchema(**item) for item in response.data]
        wines.sort(key=lambda w: (not w.wine_name.lower().startswith(wine_name.lower()), w.wine_name.lower()))
        return wines

    @staticmethod
    def create(wine: WineSchema):
        wine_dict = wine.dict()
        # Genera el UUID si no está presente o es None
        wine_dict["id"] = str(uuid.uuid4())
        response = supabase.table(WinesRepository.table_name).insert(wine_dict).execute()
        if not getattr(response, "data", None):
            return None
        return WineSchema(**response.data[0])

    @staticmethod
    def update_by_id(wine_id: int, wine_data: dict):
        # Si el campo 'id' es UUID, conviértelo a string
        if "id" in wine_data and isinstance(wine_data["id"], uuid.UUID):
            wine_data["id"] = str(wine_data["id"])
        response = supabase.table(WinesRepository.table_name).update(wine_data).eq("wine_id", wine_id).execute()
        if not getattr(response, "data", None):
            return None
        return WineSchema(**response.data[0])

    @staticmethod
    def delete_by_id(wine_id: int):
        response = supabase.table(WinesRepository.table_name).delete().eq("wine_id", wine_id).execute()
        return bool(getattr(response, "data", None))