import sqlite3
from datetime import datetime


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db
        self.create_table_users()

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if parameters is None:
            parameters = ()
        connection = self.connection
        cursor = connection.cursor()
        data = None
        try:
            cursor.execute(sql, parameters)
            if commit:
                connection.commit()
            if fetchall:
                data = cursor.fetchall()
            if fetchone:
                data = cursor.fetchone()
        except sqlite3.Error as e:
            print(f"SQL Error: {e}")  # Consider using logging instead
        finally:
            connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT,
            telegram_id TEXT UNIQUE,
            contact TEXT
        )
        """
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([f"{item} = ?" for item in parameters])
        return sql, tuple(parameters.values())


    def update_user(self, id: int, contact: str):
        sql = "UPDATE Users SET contact = ? WHERE id = ?"
        parameters = (contact, id)

        try:
            self.execute(sql, parameters=parameters, commit=True)
        except sqlite3.Error as e:
            print(f"Error updating user: {e}")

    def get_all_user_ids(self):
        sql = "SELECT id FROM Users"
        result = self.execute(sql, fetchall=True)
        return [row[0] for row in result]


    def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)


    def update_user_fullname(self, fullname: str, telegram_id: str):
        sql = "UPDATE Users SET fullname=? WHERE telegram_id=?"
        return self.execute(sql, parameters=(fullname, telegram_id), commit=True)


    def delete_users(self):
        self.execute("DELETE FROM Users", commit=True)






