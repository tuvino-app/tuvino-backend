import uuid
from fastapi import HTTPException
import logging

from repository.supabase_repository import SupabaseRepository

from models.user import User

class UsersRepository(SupabaseRepository):
    _table_name = "usuarios"

    def get_all_users(self):
        return self.session.table(self._table_name).select("*").execute()

    def get_user_by_id(self, user_uid: str):
        try:
            uuid.UUID(user_uid)
        except ValueError:
            logging.error(f'El id {user_uid} no es un UUID valido')
            raise HTTPException(status_code=400, detail="Invalid user ID format")

        usuario = self.session.table(self._table_name).select("*").eq("uid", user_uid).execute().data[0]
        if not usuario:
            logging.error(f'El usuario con id {user_uid} no existe')
            raise HTTPException(status_code=404, detail="User not found")
        return User(usuario['uid'], usuario['nombre'], usuario['email'])