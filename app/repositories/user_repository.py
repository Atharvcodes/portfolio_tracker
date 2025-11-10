from typing import Optional, Dict
from app.database import get_db_connection, get_db_cursor

class UserRepository:
    def create(self, name: str, email: str, password_hash: Optional[str] = None) -> Dict:
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(
                """
                INSERT INTO users (name, email, password_hash)
                VALUES (%s, %s, %s)
                RETURNING user_id, name, email, created_at
                """,
                (name, email, password_hash)
            )
            conn.commit()
            return dict(cursor.fetchone())
    
    def get_by_id(self, user_id: int) -> Optional[Dict]:
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(
                "SELECT user_id, name, email, created_at FROM users WHERE user_id = %s",
                (user_id,)
            )
            result = cursor.fetchone()
            return dict(result) if result else None
    
    def get_by_email(self, email: str) -> Optional[Dict]:
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(
                "SELECT user_id, name, email, password_hash, created_at FROM users WHERE email = %s",
                (email,)
            )
            result = cursor.fetchone()
            return dict(result) if result else None
