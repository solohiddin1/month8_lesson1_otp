from django.db import models
from django.db import models as m

class Student(models.Model):
    name = models.CharField()
    surname = models.CharField()
    age = models.CharField()


    def __str__(self):
        return self.name
