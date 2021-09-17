import crispy_forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, HTML, Field
from django import forms
from django.contrib.admin.helpers import Fieldset
from django.forms import ModelForm, DateInput
from center.models import center_name, area
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Field,
    Submit,
)
class DateInput(forms.DateInput):
    input_type = 'date'


class centerform(forms.ModelForm):
    class Meta:
        model = center_name
        fields = ('name',  'working_time')
        widgets = {
            'working_time': DateInput(),

        }
