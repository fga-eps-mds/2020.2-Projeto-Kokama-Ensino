from rest_framework import viewsets
from django.shortcuts import redirect
import requests
from .models import Activity, Option, Contain;
from .serializers import ActivitySerializer
import time
from decouple import config
import random
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.status import (
    HTTP_500_INTERNAL_SERVER_ERROR,
)


random.seed(time.time())

class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)

class ActivityViewSet(viewsets.ModelViewSet):
    permission_classes = (IsSuperUser,)
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    remove_chars = set([',', '.', '<', '>'])

    def _get_data(self):
        url = '{base_url}/{parameter}'.format(base_url = config('TRANSLATE_MICROSERVICE_URL'), parameter = 'traducao/frases')
        response = requests.get(url)
        response.raise_for_status()
        return response.json()


    def _clean_database(self):
        Contain.objects.all().delete()
        Option.objects.all().delete()
        Activity.objects.all().delete()


    def _add_possible_options(self, kokama_phrase):
        options = []
        for untreated_option in kokama_phrase.split():
            word = ''.join([c for c in untreated_option if c not in self.remove_chars])
            option = Option(option=word)
            options.append(option)
            if option not in Option.objects.all():
                option.save()

        return options


    def generate_random_exercises(self):
        random.seed(time.time())
        try:
            phrases = self._get_data()
        except Exception:
            return
        self._clean_database()

        for phrase in phrases:
            activity = Activity(phrase_portuguese=phrase['phrase_portuguese'], phrase_kokama=phrase['phrase_kokama'])
            activity.save()

            options = self._add_possible_options(phrase['phrase_kokama'])

            correct_option_word = random.choice(options)
            correct_option = Option.objects.filter(option=correct_option_word)[0]
            activity.options.add(correct_option)

        for phrase in phrases:
            activity = Activity.objects.filter(phrase_portuguese=phrase['phrase_portuguese'], phrase_kokama=phrase['phrase_kokama'])[0]
            correct_option = activity.options.all()[0]
            options_list = random.sample(list(Option.objects.exclude(option=correct_option)), 3)

            for option in options_list:
                activity.options.add(option)
            activity.save()

        return redirect('atividades/')