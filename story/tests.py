from django.test import TestCase
from django.apps import apps
from .models import Story
from .apps import StoryConfig


class StoryModelTest(TestCase):

    def setUp(self):
        # Ok
        Story.objects.create(
            title_portuguese='test_title_portuguese1',
            text_portuguese='test_text_portuguese1',
            title_kokama='test_title_kokama1',
            text_kokama='test_text_kokama1'
        )

        # MaxLen fail
        Story.objects.create(
            title_portuguese='test_title_portuguese with more than max_length(fifty) characters',
            text_portuguese='test_text_portuguese2',
            title_kokama='test_title_kokama with more than max_length(fifty) characters',
            text_kokama='test_text_kokama2'
        )

    def test_story_str(self):
        story = Story.objects.get(title_portuguese='test_title_portuguese1')
        self.assertEqual(str(story), 'test_title_portuguese1 <-> test_title_kokama1')

    def test_title_max_length(self):
        story_correct = Story.objects.get(title_portuguese='test_title_portuguese1')
        self.assertLessEqual(len(story_correct.title_portuguese), 50)
        self.assertLessEqual(len(story_correct.title_kokama), 50)

        story_fail = Story.objects.get(title_portuguese='test_title_portuguese with more than max_length(fifty) characters')
        self.assertGreater(len(story_fail.title_portuguese), 50)
        self.assertGreater(len(story_fail.title_kokama), 50)

class StoryConfigTest(TestCase):

    def test_apps(self):
        self.assertEqual(StoryConfig.name, 'story')
        self.assertEqual(apps.get_app_config('story').name, 'story')
