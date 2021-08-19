import crispy_forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, HTML, Field
from django import forms
from django.contrib.admin.helpers import Fieldset
from django.forms import ModelForm
from center.models import center_name, area
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Field,
    Submit,
)


class centerform(forms.ModelForm):
    class Meta:
        model = center_name
        fields = ('name', 'updated_dosses','working_time', 'doss_per_day')




# class centerform(forms.Form):
#     area_name=forms.IntegerField()
#     name = forms.CharField(required=True)
#     updated_dosses= forms.IntegerField()
#     doss_per_day=forms.IntegerField()
#     working_time = forms.DateTimeField()




