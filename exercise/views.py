from rest_framework import viewsets
from django.shortcuts import redirect
import requests
from .models import Activity, Option, Contain;
from .serializers import ActivitySerializer
import time
from decouple import config
import random
from rest_framework.status import (
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from rest_framework.response import Response


random.seed(time.time())


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    remove_chars = set([',', '.', '<', '>'])

    def get_data(self, url):
        try:
            response = requests.get(url)
        except Exception:
            return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)
        return response

    def add_possible_options(self, kokama_phrase):
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
        url = '{base_url}/{parameter}'.format(base_url = config('TRANSLATE_MICROSERVICE_URL'), parameter = 'frases')
        try:
            phrases = self._get_data(url).json()
            
        except Exception:
            return
        
        Contain.objects.all().delete()
        Option.objects.all().delete()
        Activity.objects.all().delete()

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