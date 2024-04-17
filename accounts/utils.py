import random
from django.core.mail import send_mail
from django.conf import settings

def generate_otp(length=6):
    return ''.join(str(random.randint(0, 9)) for _ in range(length))



def send_otp_email(email, otp):


    subject = 'OTP for Verification'
    message = f'Your OTP for verification is: {otp}'
    from_email = settings.EMAIL_HOST_USER
    to_email = [email]
    send_mail(subject, message, from_email, to_email)