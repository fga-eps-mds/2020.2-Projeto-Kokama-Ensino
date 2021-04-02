from django.shortcuts import render
from rest_framework import viewsets, mixins
from .models import KokamaHistory
from .serializers import KokamaHistorySerializer


class KokamaHistoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = KokamaHistory.objects.all()
    serializer_class = KokamaHistorySerializer