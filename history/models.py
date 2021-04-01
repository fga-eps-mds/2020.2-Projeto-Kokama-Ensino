from django.db import models

class KokamaHistory(models.Model):
    history_title = models.CharField(max_length= 50)
    history_text = models.TextField(null=False, blank=False)

    def __str__(self):
        return self.history_title