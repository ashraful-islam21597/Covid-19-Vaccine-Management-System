from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from staff.models import user


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = user
        fields = ('Fullname','username','staff_user','is_staff','is_superuser','is_active')
        #fields = UserCreationForm.Meta.fields +('Profilepicture',)
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = user
        fields = ('Fullname','username','staff_user')
        #fields = UserChangeForm.Meta.fields