import sqlite3

class DatabaseHelper:

    def __init__(self, databases_path: str, database_name: str):
        self.db_path = databases_path
        self.db_name = database_name
        self.is_db_exists()

    def is_db_exists(self):
        

    def create_table(self):
        pass

    def select_item(self):
        pass

    def modify_item(self):
        pass

    def delete_item(self):
        pass


