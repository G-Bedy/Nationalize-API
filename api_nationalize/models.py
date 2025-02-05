from django.db import models


class Person(models.Model):
    count = models.IntegerField()
    name = models.CharField(max_length=255, unique=True)
    country = models.JSONField()

    def __str__(self):
        return self.name

