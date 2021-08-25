from django.forms import forms

from citizen.models import people


class centerform(forms.ModelForm):
    class Meta:
        model = people
        fields = ('doss_1st', 'registered')


