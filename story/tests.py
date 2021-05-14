from django.test import TestCase
from django.apps import apps
from .models import Story
from .apps import StoryConfig


class StoryModelTest(TestCase):

    def setUp(self):
        Story.objects.create(title='test_title', text='test_text')
        Story.objects.create(title='test_title with more than max_length(fifty) characters', text='test_text')

    def test_story_str(self):
        story = Story.objects.get(title='test_title')
        self.assertEqual(str(story), 'test_title')

    def test_title_max_length(self):
        story_correct = Story.objects.get(title='test_title')
        self.assertLessEqual(len(story_correct.title), 50)

        story_fail = Story.objects.get(title='test_title with more than max_length(fifty) characters')
        self.assertGreater(len(story_fail.title), 50)

class StoryConfigTest(TestCase):

    def test_apps(self):
        self.assertEqual(StoryConfig.name, 'story')
        self.assertEqual(apps.get_app_config('story').name, 'story')