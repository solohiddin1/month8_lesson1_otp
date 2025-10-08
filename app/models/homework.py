from operator import truediv
from django.db import models


class Homework(models.Model):
    # title = models.CharField(max_length=200,blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class HomeworkUpload(models.Model):
    student = models.ForeignKey('Student',related_name='homework_upload',on_delete=models.CASCADE)
    homework = models.ForeignKey('Homework',related_name='uploads',on_delete=models.CASCADE)
    file = models.FileField(upload_to='student_homework_file/', blank=True, null=True)
    photo = models.FileField(upload_to='student_homework_photo/', blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    mark = models.SmallIntegerField(blank=True, null=True)
    is_checked = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    