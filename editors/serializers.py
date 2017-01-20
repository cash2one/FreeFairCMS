from rest_framework import serializers

from .models import Editor


class EditorDetailsSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    
    def get_role(self, obj):
        return obj.get_role_display()

    class Meta:
        model = Editor
        fields = ('email', 'role')
