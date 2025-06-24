from repository.supabase_repository import SupabaseRepository

class UsersRepository(SupabaseRepository):
    _table_name = "usuarios"

    def get_all_users(self):
        return self.session.table(self._table_name).select("*").execute()

    def get_user_by_id(self, id):
        return self.session.table(self._table_name).select("*").eq("id", id).execute()