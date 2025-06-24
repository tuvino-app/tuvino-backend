import os
import logging

from supabase import create_client, Client

class SupabaseRepository:
    def __init__(self):
        self.url: str = os.environ.get("SUPABASE_URL")
        self.key: str = os.environ.get("SUPABASE_KEY")
        logging.info(f"url: {self.url}, key: {self.key}")
        if not self.url or not self.key:
            logging.error("Missing environment variables.")
            raise Exception("Missing environment variables.")

        self.session: Client = create_client(self.url, self.key)
        if not self.session:
            logging.error("Failed to connect to database.")
            raise Exception("Connection to database failed.")