import email
from django.contrib.auth.backends import ModelBackend
from app.models.user import User

class EmailBackend(ModelBackend):

    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            print("authenticating ---")
            user = User.objects.get(email=email)
            print(user,'=====')
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None