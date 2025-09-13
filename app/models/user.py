from django.db import models

class User(models.Model):
    phone_number = models.CharField()
    email = models.CharField()
    password = models.CharField()
    is_admin = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


    def __str__(self):
        return self.phone_number
