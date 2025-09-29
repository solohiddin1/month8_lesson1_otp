from django.db import models
from app.models.teacher import Teacher
from app.models.groups import Group
from app.models.student import Student
from app.models.lessons import Lesson


class Attendence(models.Model):
    teacher_id = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    group_id = models.ForeignKey(Group,on_delete=models.CASCADE)
    absent_students = models.ManyToManyField(Student,blank=True,related_name="absents")
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE,null=True,blank=True,default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)