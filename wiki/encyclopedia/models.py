from django.db import models

class Entry(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.name
