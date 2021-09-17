from cloudinary.models import CloudinaryField
from django.db import models

class info(models.Model):
    heading=models.CharField(max_length=120)
    text=models.TextField(max_length=2000)
    upadted_at=models.DateTimeField(auto_now_add=True)
    image=CloudinaryField()
