from django.contrib.auth.models import AbstractUser
from django.db import models

class user(AbstractUser):
    Fullname=models.CharField(max_length=120)
    staff_user=models.CharField(unique=True, max_length=8)
    #password = models.CharField(max_length=8)
