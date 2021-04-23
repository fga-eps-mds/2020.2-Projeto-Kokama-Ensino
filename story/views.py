from rest_framework import viewsets
from .models import Story
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.http import JsonResponse
from decouple import config
from rest_framework.status import (
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_405_METHOD_NOT_ALLOWED,
    HTTP_400_BAD_REQUEST,
)

SERVER_ERROR = 'Erro interno do servidor'

@api_view(["POST"])
def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user != None and user.is_superuser:
        django_login(request, user)
        return Response(status=HTTP_200_OK)
    else:
        return Response(status=HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def authenticate(request):
    if request.user and request.user.is_superuser:
        user_ip = str(request.META['REMOTE_ADDR'])
        if user_ip in config('ALLOWED_IP_LIST'):
            return Response(HTTP_200_OK)

    return Response(status=HTTP_401_UNAUTHORIZED)


@require_http_methods(['GET'])
def list_story(request):
    allowed = authenticate(request)
    if allowed.status_code == HTTP_401_UNAUTHORIZED:
        return HttpResponse(
            SERVER_ERROR,
            status=HTTP_401_UNAUTHORIZED,
        )
  
    data = list(Story.objects.values())
    return JsonResponse(data, safe=False)

    

def add_story(request, id):
    pass

def delete_story(request, id):
    pass

