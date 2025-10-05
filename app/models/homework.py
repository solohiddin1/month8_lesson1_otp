from django.db import models


class Homework(models.Model):
    student = models.ForeignKey('Student',related_name='student_homework',on_delete=models.CASCADE)
    lesson = models.ForeignKey('Lesson',related_name='student_homework',on_delete=models.CASCADE)
    file = models.FileField(upload_to='student_homework_file/',blank=True,null=True)
    photo = models.FileField(upload_to='student_homework_photo/',blank=True,null=True)
    text = models.TextField(blank=True,null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
