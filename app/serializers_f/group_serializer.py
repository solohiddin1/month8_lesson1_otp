from rest_framework import serializers

from app.models.groups import Group
# from app.serializers_f.user_serializer 

class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = "__all__"
        read_only_fields = ["created_at","updated_at","is_active"]