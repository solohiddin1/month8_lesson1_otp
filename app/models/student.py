from django.db import models
from .user import User

class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='student',null=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    age = models.PositiveIntegerField()


    def __str__(self):
        return self.name
