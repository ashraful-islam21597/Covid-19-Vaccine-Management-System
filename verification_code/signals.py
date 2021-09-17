from django.db.models.signals import post_save
from django.dispatch import receiver

from citizen.models import people
from verification_code.models import code


@receiver(post_save,sender=people)
def post_save_generate_code(sender,instance,created,*args,**kwargs):
    if created:
        code.objects.create(registered_user=instance)