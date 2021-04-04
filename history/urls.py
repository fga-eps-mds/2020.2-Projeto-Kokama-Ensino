from django.urls import path
from . import views_html
from . import views

urlpatterns = [
    path('adicionar-historias/', views_html.add_history, name='add_history'),
    path('', views_html.list_history, name='list_history'),
    path('<int:id>/', views_html.views_history, name='views_history'),
    path('<int:id>/delete', views_html.del_history, name='del_history'),
    path('<int:id>/edit', views_html.edit_history, name='del_history'),
]