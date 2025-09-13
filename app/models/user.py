from django.db import models

class User(models.Model):
    phone_number = models.CharField()
    email = models.CharField()
    password = models.CharField()
    is_admin = models.BooleanField()
    is_teacher = models.BooleanField()
    is_student = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateField()


    def __str__(self):
        return self.phone_number
