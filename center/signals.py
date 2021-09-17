from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# from center.models import schedule
# from citizen.models import people
# from verification_code.models import code
#
#
# @receiver(post_save,sender=schedule)
# def post_save_generate_code(sender,instance,created,*args,**kwargs):
#     if created:
#         schedule.objects.create(registered_user=instance)