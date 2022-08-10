import datetime
from email import message
from lib2to3.pgen2 import token

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User


def send_activation_mail(user_data, request):
    user = User.objects.get(email=user_data['email'])
    current_site = get_current_site(request).domain
    mail_subject = "Verify Your Account."
    to_mail = user.email
    relativeLink = reverse('api:email-verify')
    absurl = "http://"+current_site+relativeLink+"?token="+str(token)
    messsage = f"""
Welcome to E-shop,
Hi {user.username},
Click on the link below to verify your account,
{absurl}

This is an automatically generated email. Please do not reply.
@{datetime.date.today().year} E-shop | Nairobi
    """
    email = EmailMessage(
        subject=mail_subject,
        body=message
        to = [to_mail]
    )
    email.send()