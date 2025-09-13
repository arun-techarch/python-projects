import time
import logging
import schedule
from logger import setup_logging
from jobs.db_copy import copy_table_data
from jobs.db_report_email import send_db_report
from jobs.excel_upload import upload_excel_to_db

def main():
    setup_logging()
    logger = logging.getLogger("main")
    logger.info("Application started")

    # Schedule jobs
    schedule.every().day.at("01:00").do(copy_table_data)      # Copy table daily at 1 AM
    schedule.every().day.at("15:58").do(upload_excel_to_db) # Upload Excel every Monday 7 AM
    schedule.every().day.at("16:32").do(send_db_report)       # Send DB report daily at 8 AM

    #schedule.every().minute.do(upload_excel_to_db) # Upload Excel every minutes
    #schedule.every().hour.do(upload_excel_to_db) # Upload Excel every hour
    #schedule.every().monday.at("07:00").do(upload_excel_to_db) # Upload Excel every Monday 7 AM

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()