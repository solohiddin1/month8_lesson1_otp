# import email
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from log.log import setup_logger

logger = setup_logger()

class EmailBackend(ModelBackend):

    def authenticate(self, request, email=None, password=None, **kwargs):
        # Normalize inputs
        if email is None or password is None:
            return None
        normalized_email = str(email).strip().lower()
        raw_password = str(password).strip()

        UserModel = get_user_model()
        try:
            logger.info("Authenticating email=%s", normalized_email)
            user = UserModel.objects.get(email__iexact=normalized_email)
            logger.debug('Found user: %s', user)
        except UserModel.DoesNotExist:
            return None

        if user.check_password(raw_password) and self.user_can_authenticate(user):
            logger.info('Password check passed for user %s', user)
            return user
        return None