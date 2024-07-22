import os
import smtplib
from email.mime.text import MIMEText
from contributor.models import ContributorProfile
from student.models import StudentProfile
from moderator.models import ModeratorProfile
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


def get_profile(request, **kwargs):
    """Gets the profile of the logged in user"""
    if request.user.role == 'STUDENT':
        return StudentProfile.objects.filter(user=request.user).first()
    elif request.user.role == 'CONTRIBUTOR':
        return ContributorProfile.objects.filter(user=request.user).first()
    elif request.user.role == 'MODERATOR':
        return ModeratorProfile.objects.filter(user=request.user).first()
