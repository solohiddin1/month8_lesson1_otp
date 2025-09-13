from django.db import models
from .user import User

class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='student',null=True)
    name = models.CharField()
    surname = models.CharField()
    age = models.CharField()


    def __str__(self):
        return self.name
