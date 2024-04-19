import random
from django.core.mail import send_mail
from django.conf import settings


def send_otp_to_email(email):
    otp = generate_otp()
    # print(f'Generated OTP: {otp}')
    subject = 'OTP Verification'
    message = f'Your OTP for account verification is: {otp}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
    return otp


def generate_otp():
    # Generate a 6-digit OTP
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])