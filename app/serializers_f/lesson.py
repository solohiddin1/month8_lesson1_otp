from rest_framework  import serializers
from app.models.lessons import Lesson
from app.serializers_f.homework_serializer import HomeworkSerializer

class LessonSerializer(serializers.ModelSerializer):
    # homework = HomeworkSerializer(required=False,allow_null=True)

    class Meta:
        model = Lesson
        fields = '__all__'
