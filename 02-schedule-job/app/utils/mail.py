import json
import smtplib
import logging
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)

with open("app/config.json") as f:
    config = json.load(f)

def send_mail(subject, body):
    try:
        logger.info(config)
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = config["email"]["sender"]
        msg["To"] = config["email"]["recipient"]

        with smtplib.SMTP(config["email"]["smtp_server"], config["email"]["port"]) as server:
            server.starttls()
            server.login(config["email"]["sender"], config["email"]["app_password"])
            server.sendmail(msg["From"], [msg["To"]], msg.as_string())
            logger.info("✅ Email sent successfully!")
    except Exception as e:
        logger.error(f"❌ Error: {e}")