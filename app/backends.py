# import email
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):

    def authenticate(self, request, email=None, password=None, **kwargs):
        # Normalize inputs
        if email is None or password is None:
            return None
        normalized_email = str(email).strip().lower()
        raw_password = str(password).strip()

        UserModel = get_user_model()
        try:
            print("authenticating ---")
            user = UserModel.objects.get(email__iexact=normalized_email)
            print(user, '=====')
        except UserModel.DoesNotExist:
            return None

        if user.check_password(raw_password) and self.user_can_authenticate(user):
            return user
        return None