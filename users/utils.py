import os
import smtplib
from email.mime.text import MIMEText
from django.contrib.auth.tokens import PasswordResetTokenGenerator

def send_email(dest, subject, body):
    receiver_email = dest
    sender_email = os.getenv('SCHOLARLY_EMAIL')
    password = os.getenv('EMAIL_PASSWORD')
    message = MIMEText(body)
    message["Subject"] = subject

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

def generate_reset_token(user):
    token_generator = PasswordResetTokenGenerator()
    return token_generator.make_token(user)
