from django.db import models
from app.models.user import User 
# from app.models.student import Student
from app.models.teacher import Teacher

class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    room = models.PositiveIntegerField(default=0)
    floor = models.PositiveIntegerField(default=1)
    students_set = models.ManyToManyField(
        'Student', 
        related_name='student_groups'
    )
    teacher = models.ForeignKey(
        'Teacher', 
        on_delete=models.CASCADE,
        related_name='teaching_groups'
    )
    started_day = models.DateField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    student_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=False)

    # admin = models.ForeignKey('User', on_delete=models.CASCADE, related_name='administered_groups')
    def __str__(self):
        return self.name