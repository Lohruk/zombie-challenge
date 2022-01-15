from django.core.exceptions import ValidationError
from django.db import models

gender_choices = (
    ("F", "Female"),
    ("M", "Male"),
    ("O", "Other")
)


class SurvivorNames(models.Model):
    name = models.CharField(max_length=40)


class Survivor(models.Model):
    name = models.CharField(max_length=40)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, blank=True)
    last_location_lat = models.DecimalField(max_digits=6, decimal_places=4)
    last_location_long = models.DecimalField(max_digits=6, decimal_places=4)
    fiji_water = models.IntegerField(blank=True)
    campbell_soup = models.IntegerField(blank=True)
    first_aid_pouch = models.IntegerField(blank=True)
    ak_47 = models.IntegerField(blank=True)
    infection = models.CharField(max_length=3, editable=False, default=False)
    infection_count = models.IntegerField(editable=False, default=0)

    def __str__(self):
        return self.name


class Report(models.Model):
    infected_percent = models.CharField(max_length=15)
    non_infected_percent = models.CharField(max_length=15)
    avg_water = models.CharField(max_length=15)
    avg_food = models.CharField(max_length=15)
    avg_first_aid = models.CharField(max_length=15)
    avg_gun = models.CharField(max_length=15)
    lost_points = models.CharField(max_length=15)
    report_date = models.DateField(auto_now_add=True)


class SurvivorTrade(models.Model):
    survivor_1_id = models.IntegerField(blank=True)
    survivor_2_id = models.IntegerField(blank=True)
    survivor_1_water = models.IntegerField(blank=True)
    survivor_1_soup = models.IntegerField(blank=True)
    survivor_1_first_aid = models.IntegerField(blank=True)
    survivor_1_gun = models.IntegerField(blank=True)
    survivor_2_water = models.IntegerField(blank=True)
    survivor_2_soup = models.IntegerField(blank=True)
    survivor_2_first_aid = models.IntegerField(blank=True)
    survivor_2_gun = models.IntegerField(blank=True)
