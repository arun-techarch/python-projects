import logging
import pandas as pd
from utils.db_type import DBType
from utils.db import get_connection

logger = logging.getLogger(__name__)

# Infer SQL column types
def infer_sql_type(dtype):
    if "int" in str(dtype):
        return "NUMBER"
    elif "float" in str(dtype):
        return "FLOAT"
    elif "bool" in str(dtype):
        return "BOOLEAN"
    elif "datetime" in str(dtype):
        return "TIMESTAMP"
    else:
        return "VARCHAR2(200)"

def upload_excel_to_db():
    conn = get_connection(DBType.SOURCE)
    cursor = conn.cursor()
    try:
        df = pd.read_csv("app/files/data.csv")  # fails if file missing

        columns = []
        col_defs = []
        
        for col, dtype in df.dtypes.items():
            sql_type = infer_sql_type(dtype)
            columns.append(col.upper())
            col_defs.append(f'"{col.upper()}" {sql_type}')

        create_sql = f"CREATE TABLE employee ({', '.join(col_defs)})"
        cursor.execute(create_sql)
        logger.info("Create the employee table successfully.")

        rows = [row for _, row in df.iterrows()]
        
        if rows:
            placeholders = ", ".join([":" + str(i+1) for i in range(len(columns))])
            insert_sql = f'INSERT INTO employee ({", ".join([f"{c}" for c in columns])}) VALUES ({placeholders})'

            cursor.executemany(insert_sql, rows)
            conn.commit()
            logger.info("Excel data uploaded to database successfully.")
        else:
            logger.info("No rows found in csv file.")
    except Exception as e:
        logger.error(f"Error uploading Excel data: {e}")  # triggers email alert
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
