from django.db import models
from django.db.models.fields import related
# from rest_framework.relations import PrimaryKeyRelatedField
from .user import User

class Teacher(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='teacher')
    name = models.CharField()
    surname = models.CharField()
    age = models.CharField()


    def __str__(self):
        return self.name