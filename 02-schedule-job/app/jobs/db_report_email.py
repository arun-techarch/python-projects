import logging
from utils.db_type import DBType
from utils.mail import send_mail
from utils.db import get_connection

logger = logging.getLogger(__name__)

def send_db_report():
    conn = get_connection(DBType.SOURCE)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT ID, NAME, EMAIL, PHONE, COMPANY, CITY, COUNTRY FROM CUSTOMER WHERE ROWNUM <= 10")
        rows = cursor.fetchall()
        body = "".join([f"{r[0]} - {r[1]} - {r[2]} - {r[3]} - {r[4]} - {r[5]} - {r[6]}" for r in rows])
        send_mail("DB Report", body)
        logger.info("DB report email sent successfully.")
    except Exception as e:
        logger.error(f"Error sending DB report: {e}")
    finally:
        cursor.close()
        conn.close()
