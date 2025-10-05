from django.db import models
from app.models.groups import Group
from .user import User

class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='student',null=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    # homework = models.ForeignKey('Homework',on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name
