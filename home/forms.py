from django.forms import ModelForm

from user.models import user


class registrationForm(ModelForm):
    class Meta:
        model = user
        fields = ('nid','center','period',)