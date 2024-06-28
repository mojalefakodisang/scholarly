import os
import smtplib
from email.mime.text import MIMEText

def send_email(dest, subject, body):
    receiver_email = dest
    sender_email = os.environ.get('SCHOLARLY_EMAIL')
    password = os.environ.get('EMAIL_PASSWORD')
    message = MIMEText(body)
    message["Subject"] = subject

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())