from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin

from staff.forms import CustomUserCreationForm, CustomUserChangeForm
from staff.models import user
class CustomUserAdmin(UserAdmin):
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    # model=user
    list_display = ['username','password', 'is_staff', ]
admin.site.register(user, CustomUserAdmin)

