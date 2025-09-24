from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_delete, sender = settings.AUTH_USER_MODEL)
def delete_user_token(sender, instance, **kwargs):
    try:
        token = Token.objects.get(user=instance)
        token.delete()
        print(f"Token deleted successfully for user {instance}.")
    except Token.DoesNotExist:
        pass