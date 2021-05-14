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
    HTTP_200_OK,
)
from rest_framework.response import Response


random.seed(time.time())


class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
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

    def generate_random_exercises(self, url):
        view_set = ActivityViewSet()
        random.seed(time.time())
        try:
            phrases = view_set.get_data(url).json()
        except Exception:
            return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)
        
        # SQLite does not handle many operations at once
        for contain in Contain.objects.all():
            contain.delete()
        for option in Option.objects.all():
            option.delete()
        for activity in Activity.objects.all():
            activity.delete()

        for phrase in phrases:
            activity = Activity.objects.create(phrase_portuguese=phrase['phrase_portuguese'], phrase_kokama=phrase['phrase_kokama'])

            options = view_set.add_possible_options(activity.phrase_kokama)
            correct_option = random.choice(options)
            activity.options.add(correct_option)

        for activity in Activity.objects.all():
            correct_option = str(activity.options.all().first())
            filtered_options = []

            for option in Option.objects.exclude(option=correct_option):
                if activity.phrase_kokama.find(str(option)) == -1:
                    filtered_options.append(option)

            options_list = random.sample(filtered_options, 3)
            for option in options_list:
                activity.options.add(option)

            activity.save()

        return Response(status=HTTP_200_OK)


    def run(self):
        url = '{base_url}/{parameter}'.format(base_url = config('TRANSLATE_MICROSERVICE_URL'), parameter = 'frases/')
        self.generate_random_exercises(url)
