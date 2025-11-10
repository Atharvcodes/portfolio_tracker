from typing import List, Dict
from datetime import date
from app.database import get_db_connection, get_db_cursor

class TransactionRepository:
    def create(self, user_id: int, symbol: str, transaction_type: str, 
               units: int, price: float, transaction_date: date) -> Dict:
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(
                """
                INSERT INTO transactions (user_id, symbol, transaction_type, units, price, transaction_date)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING transaction_id, user_id, symbol, transaction_type, units, price, transaction_date, created_at
                """,
                (user_id, symbol.upper(), transaction_type, units, price, transaction_date)
            )
            conn.commit()
            return dict(cursor.fetchone())
    
    def get_by_user(self, user_id: int) -> List[Dict]:
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(
                """
                SELECT transaction_id, user_id, symbol, transaction_type, units, price, transaction_date, created_at
                FROM transactions
                WHERE user_id = %s
                ORDER BY transaction_date DESC, created_at DESC
                """,
                (user_id,)
            )
            return [dict(row) for row in cursor.fetchall()]
    
    def get_by_user_and_symbol(self, user_id: int, symbol: str) -> List[Dict]:
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(
                """
                SELECT transaction_id, user_id, symbol, transaction_type, units, price, transaction_date, created_at
                FROM transactions
                WHERE user_id = %s AND symbol = %s
                ORDER BY transaction_date DESC, created_at DESC
                """,
                (user_id, symbol.upper())
            )
            return [dict(row) for row in cursor.fetchall()]
