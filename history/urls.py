from django.urls import path
from . import views_HTML

urlpatterns = [
    path('adicionar-historias/', views_HTML.add_history, name='add_history'),
    path('', views_HTML.list_history, name='list_history'),
]