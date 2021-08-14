from django.forms import ModelForm

from citizen.models import people


class registrationForm(ModelForm):
    class Meta:
        model = people
        fields = ('nid','center','period',)