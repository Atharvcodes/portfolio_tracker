import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from .config import settings

connection_pool = None

def init_pool():
    global connection_pool
    try:
        connection_pool = psycopg2.pool.SimpleConnectionPool(
            minconn=1,
            maxconn=20,
            host=settings.db_host,
            port=settings.db_port,
            database=settings.db_name,
            user=settings.db_user,
            password=settings.db_password
        )
        print("Database connection pool initialized")
    except Exception as e:
        print(f"Failed to initialize connection pool: {e}")
        raise

@contextmanager
def get_db_connection():
    if connection_pool is None:
        raise Exception("Connection pool not initialized")
    
    conn = connection_pool.getconn()
    try:
        yield conn
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        connection_pool.putconn(conn)

def get_db_cursor(conn):
    return conn.cursor(cursor_factory=RealDictCursor)
