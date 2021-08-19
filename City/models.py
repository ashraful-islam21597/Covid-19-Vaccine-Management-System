from django.db import models

class area(models.Model):
    name = models.CharField(max_length=120)
    population = models.IntegerField(default=0)
    total_vaccinated = models.IntegerField(default=0)
    priority = models.FloatField(default=0)
    total_rgistered = models.IntegerField(default=0)
    doss_1st_done = models.IntegerField(default=0)

    def __str__(self):
        return self.name
