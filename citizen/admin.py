from django.contrib import admin

from citizen.models import people, Registration_pending

admin.site.register(people)
admin.site.register(Registration_pending)
