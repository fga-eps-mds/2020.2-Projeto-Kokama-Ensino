from rest_framework import serializers
from .models import Story

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['id',
                  'title_portuguese', 'text_portuguese',
                  'title_kokama', 'text_kokama']