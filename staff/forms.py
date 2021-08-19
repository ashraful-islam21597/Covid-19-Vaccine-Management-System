from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from staff.models import user, center_staff


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

class Center_staff_form(ModelForm):
    class Meta:
        model = center_staff
        fields = ('name','username','password')
        #fields = UserCreationForm.Meta.fields +('Profilepicture',)