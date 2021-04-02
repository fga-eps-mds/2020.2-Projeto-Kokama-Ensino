from rest_framework import serializers
from .models import KokamaHistory



class KokamaHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = KokamaHistory
        fields = ['history_title', 'history_text']