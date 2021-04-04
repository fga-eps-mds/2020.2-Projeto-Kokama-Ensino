from django.db import models

class KokamaHistory(models.Model):
    history_title = models.CharField(max_length=50)
    history_text = models.TextField()

    def __str__(self):
        return self.history_title

    