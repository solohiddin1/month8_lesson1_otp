from rest_framework  import serializers
from app.models.homework import Homework
from app.models.lessons import Lesson

class LessonSerializer(serializers.ModelSerializer):
    homework = serializers.PrimaryKeyRelatedField(
        queryset = Homework.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Lesson
        fields = '__all__'
