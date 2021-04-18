"""learn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from django.conf.urls import include, url
from exercise.views import ActivityViewSet
from story.views import StoryViewSet

router = routers.DefaultRouter()
router.register(r'atividades', ActivityViewSet, basename="activities")
router.register(r'lista_de_historias', StoryViewSet, basename="stories")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('historia/', include(router.urls)),
]


from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()
activity = ActivityViewSet()
scheduler.add_job(activity.generate_random_exercises, "cron", day_of_week="sun", hour=0, id="update_activities", replace_existing=True)
scheduler.start()