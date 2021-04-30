from django.db import models


class Story(models.Model):
    title_portuguese = models.CharField(max_length=50)
    text_portuguese = models.TextField()

    title_kokama = models.CharField(max_length=50, blank=True)
    text_kokama = models.TextField(blank=True)

    def __str__(self):
        return self.title_portuguese + " <-> " + self.title_kokama
