from .models import Story
from decouple import config
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from .serializers import StoryListSerializer
from rest_framework.generics import (
    ListCreateAPIView,
    UpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

SERVER_ERROR = 'Erro interno do servidor'


@require_http_methods(['GET', 'POST', 'PUT', 'DELETE'])
def authenticate(request):
    print('Autenticando')
    if request.user and request.user.is_superuser:
        print('Você é um super usuário')
        user_ip = str(request.META['REMOTE_ADDR'])
        if user_ip in config('ALLOWED_IP_LIST'):
            print('Seu IP é permitido')
            return Response(HTTP_200_OK)

    print('Você não é super ou seu IP não é permitido')
    return Response(status=HTTP_401_UNAUTHORIZED)


class StoryList(ListCreateAPIView):
    queryset = Story.objects.all().order_by('-id')
    serializer_class = StoryListSerializer

    def get(self, request, *args, **kwargs):
        allowed = authenticate(request)
        if allowed.status_code == HTTP_401_UNAUTHORIZED:
            return HttpResponse(
                SERVER_ERROR,
                status=HTTP_401_UNAUTHORIZED,
            )
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        allowed = authenticate(request)
        if allowed.status_code == HTTP_401_UNAUTHORIZED:
            return HttpResponse(
                SERVER_ERROR,
                status=HTTP_401_UNAUTHORIZED,
            )
        try:
            if Story.objects.filter(title=request.POST.get('title')).first():
                print("Já existe")
                return Response(
                    {'error': 'Já existe uma história cadastrada com esse título.'},
                    status=HTTP_400_BAD_REQUEST,
                )
        except Exception:
            return Response(
                SERVER_ERROR,
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )

        print("Tô criando")
        story = Story.objects.create(
            title = request.POST.get('title'),
            text = request.POST.get('text')
        )
        story.save()
        return self.list(request, *args, **kwargs)


class StoryView(RetrieveUpdateDestroyAPIView):
    queryset = Story.objects.all()
    serializer_class = StoryListSerializer

    def get(self, request, *args, **kwargs):
        allowed = authenticate(request)
        if allowed.status_code == HTTP_401_UNAUTHORIZED:
            return HttpResponse(
                SERVER_ERROR,
                status=HTTP_401_UNAUTHORIZED,
            )
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        allowed = authenticate(request)
        if allowed.status_code == HTTP_401_UNAUTHORIZED:
            return HttpResponse(
                SERVER_ERROR,
                status=HTTP_401_UNAUTHORIZED,
            )
        # try:
        #     if len(Story.objects.filter(title=request.POST.get('title'))) > 1:
        #         print("Já existe")
        #         return Response(
        #             {'error': 'Já existe uma história cadastrada com esse título.'},
        #             status=HTTP_400_BAD_REQUEST,
        #         )
        # except Exception:
        #     return HttpResponse(
        #         SERVER_ERROR,
        #         status=HTTP_500_INTERNAL_SERVER_ERROR,
        #     )

        return self.update(request, *args, **kwargs)


    def delete(self, request, *args, **kwargs):
        allowed = authenticate(request)
        if allowed.status_code == HTTP_401_UNAUTHORIZED:
            pass
            return HttpResponse(
                SERVER_ERROR,
                status=HTTP_401_UNAUTHORIZED,
            )
        return self.destroy(request, *args, **kwargs)
