from django.db import models


# class area(models.Model):
#     name = models.CharField(max_length=120)
#     population = models.IntegerField(default=0)
#     total_vaccinated = models.IntegerField(default=0)
#     priority = models.IntegerField(default=0)
#     total_rgistered = models.IntegerField(default=0)
#     doss_1st_done = models.IntegerField(default=0)
#
#     def __str__(self):
#         return self.name
from City.models import area


class center_name(models.Model):
    area_name = models.ForeignKey(area, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    updated_dosses = models.IntegerField(default=0)
    available_dosses = models.IntegerField(default=0)
    doss_per_day = models.IntegerField(default=0)
    num_of_dosses = models.IntegerField(default=0)
    updated_time = models.DateField(auto_now_add=True)
    working_time = models.DateField(auto_now_add=False)
    pending_doss_center=models.IntegerField(default=0)
    total_doss_center=models.IntegerField(default=0)

    def __str__(self):
        return self.name


class period_of_dosses(models.Model):
    center_name = models.ManyToManyField(center_name)
    slot = models.CharField(max_length=2)
    target_user = models.IntegerField(default=2)
    num_user = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=False)
    start_time = models.TimeField(auto_now_add=False)
    end_time = models.TimeField(auto_now_add=False)

    def __str__(self):
        return self.slot

    def sttime(self):
        return str(self.start_time)

    def etime(self):
        return str(self.end_time)
