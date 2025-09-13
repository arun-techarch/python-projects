import json
import logging
import oracledb
from utils.db_type import DBType
from contextlib import contextmanager

logger = logging.getLogger(__name__)

with open("app/config.json") as f:
    config = json.load(f)

def get_connection(type:DBType):
    if type == DBType.SOURCE:
        dbConfig = config["oracle"][0]
    else:
        dbConfig = config["oracle"][1]

    dsn = f"{dbConfig['host']}:{dbConfig['port']}/{dbConfig['service_name']}"
    return oracledb.connect(user=dbConfig['username'], password=dbConfig['password'], dsn=dsn)

@contextmanager
def get_cursor(type = DBType.SOURCE):
    conn = get_connection(type)
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
        logger.info("Successfully executed the query")
    except Exception as e:
        logger.error("Failure to execute the query:", e)
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()