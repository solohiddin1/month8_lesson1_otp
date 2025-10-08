from django.db import models
from config.config import settings
from app.models.teacher import Teacher
from app.models.groups import Group
from app.models.homework import Homework

class Lesson(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    homework = models.ForeignKey(Homework,on_delete=models.CASCADE,blank=True,null=True,related_name='lesson_homework')
    video_url = models.FileField(upload_to=settings.VIDEO_PATH, blank=True, null=True,default=settings.DEFAULT_VIDEO_PATH)
    image = models.ImageField(upload_to=settings.PHOTO_PATH, blank=True, null=True,default=settings.DEFAULT_PHOTO_PATH)
    start_time = models.TimeField(default=None)
    end_time = models.TimeField(default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name='lessons')
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name='lessons')
    # student_homework = models.ForeignKey('Homework',on_delete=models.CASCADE,blank=True,null=True)


    def __str__(self):
        return self.title