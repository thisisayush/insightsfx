from .models import User
from apps.core.utils import send_mail
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from apps.core.utils import getOption
from django.utils import six
def UserExistsByEmail(email):
    try:
        User.objects.get(email = email)
        return True
    except User.DoesNotExist:
        return False

def sendPasswordResetEmail(user_email):

    if not UserExistsByEmail(user_email):
        return False
    user = User.objects.get(email = user_email)
    context = {
        'user': user,
        'domain': getOption('site_url'),
        'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
        'token': PasswordResetTokenGenerator().make_token(user),
        'protocol': 'http'
    }

    subject = "Reset your Password"

    if send_mail(subject, user.email, 'accounts/email/forgot-password', context):
        return True
    else:
        return False

def ActivateUserAccount(user):
    try:
        user.email_confirmed = True
        user.save()
        return True
    except Exception:
        return False

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.email_confirmed)
        )

def SendAccountActivationEmail(user_email):
    
    if not UserExistsByEmail(user_email):
        return False
    user = User.objects.get(email = user_email)
    context = {
        'user': user,
        'domain': getOption('site_url'),
        'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
        'token': AccountActivationTokenGenerator().make_token(user)
    }

    subject = "Activate your account"

    if send_mail(subject, user.email, 'accounts/email/signup', context):
        return True
    else:
        return False
