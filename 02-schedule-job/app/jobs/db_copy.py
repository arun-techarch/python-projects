import logging
from utils.db_type import DBType
from utils.db import get_connection

logger = logging.getLogger(__name__)

def copy_table_data(source_table='CUSTOMER', target_table='CUSTOMER'):
    source_conn = None
    target_conn = None
    try:
        # --- Connect to both DBs ---
        source_conn = get_connection(DBType.SOURCE)
        target_conn = get_connection(DBType.TARGET)

        src_cursor = source_conn.cursor()
        tgt_cursor = target_conn.cursor()

        # --- 1. Fetch column metadata from source table ---
        logger.info(f"Retrieving column metadata from the source {source_table} table.")
        src_cursor.execute(f"SELECT * FROM {source_table} WHERE ROWNUM = 1")
        col_names = [desc[0] for desc in src_cursor.description]

        # --- 2. Check if target table exists ---
        tgt_cursor.execute("""
            SELECT COUNT(*)
            FROM user_tables
            WHERE table_name = :tname
        """, [target_table.upper()])
        exists = tgt_cursor.fetchone()[0] > 0
        logger.info(f"{target_table} was exists: {exists}.")

        # --- 3. Create table dynamically if not exists ---
        if not exists:
            # Get column types from source
            src_cursor.execute(f"""
                SELECT column_name, data_type, data_length
                FROM user_tab_columns
                WHERE table_name = :tname
            """, [source_table.upper()])
            cols = src_cursor.fetchall()

            col_defs = []
            for cname, dtype, length in cols:
                if dtype in ("VARCHAR2", "CHAR"):
                    col_defs.append(f"{cname} {dtype}({length})")
                else:
                    col_defs.append(f"{cname} {dtype}")
            create_sql = f"CREATE TABLE {target_table} ({', '.join(col_defs)})"
            tgt_cursor.execute(create_sql)
            logger.info(f"Target table {target_table} created.")

        # --- 4. Copy data from source to target ---
        src_cursor.execute(f"SELECT * FROM {source_table}")
        rows = src_cursor.fetchall()

        if rows:
            placeholders = ", ".join([":" + str(i+1) for i in range(len(col_names))])
            insert_sql = f"INSERT INTO {target_table} ({', '.join(col_names)}) VALUES ({placeholders})"

            tgt_cursor.executemany(insert_sql, rows)
            target_conn.commit()
            logger.info(f"Copied {len(rows)} rows from {source_table} to {target_table}.")
        else:
            logger.info("No rows found in source table.")

    except Exception as e:
        logger.error(f"Error copying data: {e}")
        if target_conn:
            target_conn.rollback()
    finally:
        if source_conn:
            source_conn.close()
        if target_conn:
            target_conn.close()
