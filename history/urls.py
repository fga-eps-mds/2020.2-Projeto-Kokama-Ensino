from django.urls import path
from . import views_html
from . import views

urlpatterns = [
    path('adicionar-historias/', views_html.add_history, name='add_history'),
    path('', views_html.list_history, name='list_history'),
]