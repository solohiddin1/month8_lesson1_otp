from email.policy import default
from django.db import models
from config.config import settings
from app.models.teacher import Teacher
from app.models.groups import Group


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    homework = models.TextField(blank=True, null=True)
    video_url = models.FileField(upload_to=settings.VIDEO_PATH, blank=True, null=True,default=settings.DEFAULT_VIDEO_PATH)
    image = models.ImageField(upload_to=settings.PHOTO_PATH, blank=True, null=True,default=settings.DEFAULT_PHOTO_PATH)
    start_time = models.TimeField(default=None)
    end_time = models.TimeField(default=None)
    days_week = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name='lessons')
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name='lessons')

    def __str__(self):
        return self.title