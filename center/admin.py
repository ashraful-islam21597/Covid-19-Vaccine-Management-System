from django.contrib import admin


from center.models import center_name, period_of_dosses, area

admin.site.register(area)
admin.site.register(center_name)
admin.site.register(period_of_dosses)

