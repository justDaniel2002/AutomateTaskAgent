from client.db.database import get_db_connection
from contextlib import contextmanager


class DatabaseService:
        

    @contextmanager
    def transaction(self):

        conn = get_db_connection()

        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def execute(self, query: str, params=()):
        with self.transaction() as conn:
            cursor = conn.execute(query, params)
            return cursor

    def get_one(self, query: str, params=()):
        with self.transaction() as conn:
            cursor = conn.execute(query, params)
            row = cursor.fetchone()
        return dict(row) if row else None

    def get_all(self, query: str, params=()):
        with self.transaction() as conn:
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows] 
