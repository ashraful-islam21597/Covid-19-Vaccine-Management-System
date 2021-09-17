import random

from django.contrib.auth.models import AbstractUser
from django.db import models

from center.models import center_name


class user(AbstractUser):
    Fullname=models.CharField(max_length=120)
    staff_user=models.CharField(unique=True, max_length=8)
    is_area_manager=models.BooleanField(default=False)
    is_cnter_staff=models.BooleanField(default=False)
class center_staff(models.Model):
    staff=models.ForeignKey(center_name,on_delete=models.CASCADE)
    username=models.CharField(max_length=120)
    name=models.CharField(max_length=120)
    password=models.CharField(max_length=120)

    def __str__(self):
        return  self.name


