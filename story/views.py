from .models import Story
from .serializers import StorySerializer
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from decouple import config
from rest_framework import generics, viewsets, mixins
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_200_OK,
    HTTP_204_NO_CONTENT
)

SERVER_ERROR = 'Erro interno do servidor'
UNAUTHORIZED_ERROR = 'Você não tem autorização'

def authenticate(user_ip):
    if user_ip in config('ALLOWED_IP_LIST'):
        return True
    else:
        return False


class StoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Story.objects.all().order_by('-id')
    serializer_class = StorySerializer

    def create(self, request, *args, **kwargs):
        has_portuguese = request.POST.get('title_portuguese') and request.POST.get('text_portuguese')
        has_kokama = request.POST.get('title_kokama') and request.POST.get('text_kokama')
        ip = request.META['REMOTE_ADDR']
        
        if not authenticate(ip):
            return HttpResponse(
                UNAUTHORIZED_ERROR,
                status=HTTP_403_FORBIDDEN,
            )
        try:
            if has_portuguese or has_kokama:
                try:
                    Story.objects.create(
                        title_portuguese=request.POST.get('title_portuguese'),
                        text_portuguese=request.POST.get('text_portuguese'),
                        title_kokama=request.POST.get('title_kokama'),
                        text_kokama=request.POST.get('text_kokama')
                    )
                except Exception:
                    return Response(HTTP_500_INTERNAL_SERVER_ERROR)

                return Response(HTTP_200_OK) 
            else:
                return Response(HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=HTTP_200_OK)


    def update(self, request, *args, **kwargs):
        has_portuguese = request.data.get('title_portuguese') and request.data.get('text_portuguese')
        has_kokama = request.data.get('title_kokama') and request.data.get('text_kokama')
        ip = request.META['REMOTE_ADDR']

        if not authenticate(ip):
            return HttpResponse(
                UNAUTHORIZED_ERROR,
                status=HTTP_403_FORBIDDEN,
            )
        try:
            if has_portuguese or has_kokama:
                story = self.get_object()
                try:
                    story.title_portuguese = request.data.get('title_portuguese')
                    story.text_portuguese = request.data.get('text_portuguese')
                    story.title_kokama = request.data.get('title_kokama')
                    story.text_kokama = request.data.get('text_kokama')
                    story.save()
                except Exception:
                    return Response(HTTP_500_INTERNAL_SERVER_ERROR)

                return Response(HTTP_200_OK) 
            else:
                return Response(HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        ip = request.META['REMOTE_ADDR']
        if not authenticate(ip):
            return HttpResponse(
                UNAUTHORIZED_ERROR,
                status=HTTP_403_FORBIDDEN,
            )
        try:
            story = self.get_object()
            story.delete()
        except Exception:
            return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=HTTP_204_NO_CONTENT)
