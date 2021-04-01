from django.urls import path
from . import views_HTML

urlpatterns = [
    path('', views_HTML.add_history, name='add_history'),
]