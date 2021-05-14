from django.apps import AppConfig
import sys

class ExerciseConfig(AppConfig):
    name = 'exercise'

    def ready(self):
        if 'runserver' not in sys.argv:
            return True

        from apscheduler.schedulers.background import BackgroundScheduler
        from exercise.views import ActivityViewSet
        scheduler = BackgroundScheduler()
        activity = ActivityViewSet()
        # scheduler.add_job(activity.run, "interval", minutes = 1, id="update_activities", replace_existing=True)
        scheduler.add_job(activity.run, "cron", day_of_week="sun", hour=0, id="update_activities", replace_existing=True)
        scheduler.start()
