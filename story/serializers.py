from rest_framework import serializers
from .models import Story

class StoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['id', 'title', 'text']
