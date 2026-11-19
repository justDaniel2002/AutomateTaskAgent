from client.db.database import get_db_connection


class DatabaseService:

    def __init__(self):
        self.conn = get_db_connection()

    def execute(self, query: str, params=()):
        cursor = self.conn.execute(query, params)
        return cursor

    def get_one(self, query: str, params=()):
        cursor = self.conn.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_all(self, query: str, params=()):
            cursor = self.conn.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows] 
