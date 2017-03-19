from rest_framework import serializers
from rest_framework.fields import ChoiceField

from .models import Editor
from pages.models.pages import StatePage
from pages.api_views import get_state_page


class StatePageSimpleSerializer(serializers.ModelSerializer):
    state_display = serializers.SerializerMethodField()

    def get_state_display(self, obj):
        return obj.get_state_display()
    
    class Meta:
        model = StatePage
        fields = ('state', 'state_display')


class ChoiceDisplayField(ChoiceField):
    """
    Like ChoiceField, but gives display name instead of key.
    Still expects key for saving
    """
    def to_representation(self, value):
        if value in ('', None):
            return value
        return self.choices.get(value, value)


class EditorDetailsSerializer(serializers.ModelSerializer):
    states = StatePageSimpleSerializer(many=True, required=False)
    role = ChoiceDisplayField(choices=Editor.EDITOR_ROLES)

    def create(self, validated_data):
        states = validated_data.pop('states')

        editor = Editor(**validated_data)
        editor.set_password('freefair')
        editor.save()
     
        for state in states:
            state = get_state_page(state['state'], self.context['request'].user)
            editor.states.add(state)

        return editor

    class Meta:
        model = Editor
        fields = ('email', 'role', 'states', 'id')
