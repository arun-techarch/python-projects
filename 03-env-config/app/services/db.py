import oracledb
from app.config import get_config
from contextlib import contextmanager

config = get_config()

def get_connection():
    return oracledb.connect(user=config.oracle_user, password=config.oracle_password, dsn=config.oracle_dsn)

@contextmanager
def get_cursor():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()