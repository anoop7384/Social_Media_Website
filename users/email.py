from django.core.mail import send_mail
import random
from django.conf import settings
from .models import Profile
from django.contrib.auth.models import User


def sendEmailOTP(email):
    subject = 'Your email verification email'
    otp = random.randint(1000, 9999)
    message = 'Your otp is '+ str(otp)
    print(message)
    from_email = settings.EMAIL_HOST_USER
    # send_mail(subject, message, from_email, [email])
    user_obj = User.objects.get(email=email)
    user_obj.profile.otp = otp
    user_obj.profile.isVerified = False
    user_obj.save()