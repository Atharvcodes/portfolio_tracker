from typing import Optional, Dict
from app.database import get_db_connection, get_db_cursor

class PriceRepository:
    def get_by_symbol(self, symbol: str) -> Optional[Dict]:
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(
                "SELECT symbol, current_price, updated_at FROM prices WHERE symbol = %s",
                (symbol.upper(),)
            )
            result = cursor.fetchone()
            return dict(result) if result else None
    
    def get_all(self) -> Dict[str, float]:
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute("SELECT symbol, current_price FROM prices")
            return {row['symbol']: float(row['current_price']) for row in cursor.fetchall()}
    
    def update(self, symbol: str, price: float) -> Dict:
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(
                """
                INSERT INTO prices (symbol, current_price, updated_at)
                VALUES (%s, %s, NOW())
                ON CONFLICT (symbol) DO UPDATE
                SET current_price = EXCLUDED.current_price, updated_at = NOW()
                RETURNING symbol, current_price, updated_at
                """,
                (symbol.upper(), price)
            )
            conn.commit()
            return dict(cursor.fetchone())
