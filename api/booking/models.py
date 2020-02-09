from django.contrib.postgres.fields import ArrayField
from django.db import models


class Row(models.Model):
    name = models.CharField(max_length=1024)
    no_of_seats = models.IntegerField()
    aisle_seats = ArrayField(models.IntegerField())

    def __str__(self):
        return str(str(self.id) + ": " + self.name)


class Screen(models.Model):
    name = models.CharField(max_length=1024, unique=True)
    rows = models.ManyToManyField(Row, blank=True)

    def __str__(self):
        return str(str(self.id) + ": " + self.name)


class Reserve(models.Model):
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name="screen_reserve")
    row = models.ForeignKey(Row, on_delete=models.CASCADE, related_name="row_reserve")
    seats_reserved = ArrayField(models.IntegerField())

    def __str__(self):
        return str(self.id)
