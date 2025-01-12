import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

def send_email(to: str, subject: str, body: str):
    try:
        msg = MIMEMultipart()
        msg["From"] = os.getenv("EMAIL_FROM")
        msg["To"] = to
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT")))
        server.starttls()
        server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASSWORD"))
        server.sendmail(os.getenv("EMAIL_FROM"), to, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        raise Exception(f"Failed to send email: {str(e)}")