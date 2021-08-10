from django.db import models

from center.models import center_name, period_of_dosses


class user(models.Model):
    center=models.ForeignKey(center_name,on_delete=models.CASCADE)
    period=models.ForeignKey(period_of_dosses,on_delete=models.CASCADE)
    nid=models.CharField(unique=True,max_length=14)

    def __str__(self):
        return self.nid
    def name_of_center(self):
        return
