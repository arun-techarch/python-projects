import oracledb
import logging
from app.config import get_config
from contextlib import contextmanager

logger = logging.getLogger(__name__)
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
        logger.info("Query executed successfully")
    except Exception as e:
        conn.rollback()
        logger.error("Error in executing the query:", e)
        raise e
    finally:
        cursor.close()
        conn.close()