from rest_framework import viewsets
from .models import Story
from .serializers import StorySerializer

from rest_framework.permissions import IsAdminUser
class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)

class StoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsSuperUser,)
    queryset = Story.objects.all().order_by('-id')
    serializer_class = StorySerializer
