from django.db import models


class area(models.Model):
    name = models.CharField(max_length=120)
    population = models.IntegerField(default=0)
    total_vaccinated = models.IntegerField(default=0)
    priority = models.FloatField(default=0)
    total_rgistered = models.IntegerField(default=0)
    doss_1st_done = models.IntegerField(default=0)
    available_doss = models.IntegerField(default=0)
    pending_doss = models.IntegerField(default=0)
    total_doss_area = models.IntegerField(default=0)
    number_of_center = models.IntegerField(default=0)
    enability=models.BooleanField(default=0)

    def __str__(self):
        return self.name


class dosses_for_dhaka(models.Model):
    dosses = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
