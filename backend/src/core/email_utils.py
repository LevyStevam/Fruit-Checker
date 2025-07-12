import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv('src/core/.env')

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
print(EMAIL_ADDRESS, EMAIL_PASSWORD)

def send_email_notification(to_email: str, subject: str, body: str):
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        raise Exception('EMAIL_ADDRESS ou EMAIL_PASSWORD não configurados no .env')
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg.set_content(body)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg) 