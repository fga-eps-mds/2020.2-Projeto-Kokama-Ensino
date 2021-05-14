from django.test import TestCase
from django.apps import apps
from .models import Activity, Option, Contain
from .apps import ExerciseConfig
from .views import ActivityViewSet
import requests
from decouple import config


KOKAMA_PHRASE = 'Kokama phrase'
TEST_OPTION = 'test_option'

# Models

class ActivityModelTest(TestCase):
    def setUp(self):
        activity = Activity.objects.create(
            phrase_kokama=KOKAMA_PHRASE,
            phrase_portuguese='Portuguese phrase'
        )
    
        for i in range(4):
            option = Option.objects.create(option=TEST_OPTION+'_{}'.format(i))
            activity.options.add(option)

        activity.save()
        
    def test_activity_str(self):
        activity = Activity.objects.get(phrase_kokama=KOKAMA_PHRASE)
        self.assertEqual(str(activity), KOKAMA_PHRASE)

    def test_activity_options_length(self):
        activity = Activity.objects.get(phrase_kokama=KOKAMA_PHRASE)
        self.assertEqual(activity.options.all().count(), 4)
        

class OptionModelTest(TestCase):
    def setUp(self):
        Option.objects.create(option=TEST_OPTION)
        
    def test_option_str(self):
        option = Option.objects.get(option=TEST_OPTION)
        self.assertEqual(str(option), TEST_OPTION)

    def test_option_max_length(self):
        option_correct = Option.objects.get(option=TEST_OPTION)
        self.assertLessEqual(len(option_correct.option), 50)

        option_fail = Option.objects.create(option='option with more than max_length(fifty) characters in it')
        self.assertGreater(len(option_fail.option), 50)


class ContainModelTest(TestCase):
    def setUp(self):
        activity = Activity.objects.create(
            phrase_kokama=KOKAMA_PHRASE,
            phrase_portuguese='Portuguese phrase'
        )
        option = Option.objects.create(option=TEST_OPTION)
        activity.options.set(4*[option])
        activity.save()

        Contain.objects.create(activity=activity, options=option)
        
    def test_contain_str(self):
        activity = Activity.objects.get(phrase_kokama=KOKAMA_PHRASE)
        option = Option.objects.get(option=TEST_OPTION)
        contain = Contain.objects.filter(activity=activity, options=option).first()
        self.assertEqual(str(contain), KOKAMA_PHRASE + ' <-> ' + TEST_OPTION)


# Apps

class ExerciseConfigTest(TestCase):

    def test_apps(self):
        self.assertEqual(ExerciseConfig.name, 'exercise')
        self.assertEqual(apps.get_app_config('exercise').name, 'exercise')

    
# Views

class ActivityViewSetTest(TestCase):
        
    remove_chars = set([',', '.', '<', '>'])
    mocked_url = 'https://6093298ca7e53a00179508bb.mockapi.io/frases'

    def test_get_data(self):
        response = ActivityViewSet.get_data(ActivityViewSet, self.mocked_url)
        self.assertEqual(response.status_code, 200)

        response = ActivityViewSet.get_data(ActivityViewSet, 'wrong_url')
        self.assertEqual(response.status_code, 500)

    def test_add_possible_options(self):
        kokama_phrase = 'I, love, panara <a lot>.'
        expected = ['I', 'love', 'panara', 'a', 'lot']
        options = ActivityViewSet.add_possible_options(ActivityViewSet, kokama_phrase)
        result = []
        for option in options:
            result.append(str(option))
        self.assertEqual(result, expected)

    def test_generate_random_exercises(self):
        response = ActivityViewSet.generate_random_exercises(ActivityViewSet, 'wrong_url')
        self.assertEqual(response.status_code, 500)

        ActivityViewSet.generate_random_exercises(ActivityViewSet, self.mocked_url)
        for activity in Activity.objects.all():
            self.assertEqual(activity.options.all().count(), 4)
            for option in activity.options.all():
                if activity.phrase_kokama.find(str(option)):
                    result = True
            self.assertEqual(result, True)