from django.db import models

class kokamaHistory(models.Model):
    history_title = models.CharField(max_length= 50)
    history_text = models.TextField(null=False, blank=False)

    def __str__(self):
        return '%s <-> %s' % (self.history_title, self.history_text)
