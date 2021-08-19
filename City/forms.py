from django.forms import ModelForm

from City.models import area


class areaform(ModelForm):
    class Meta:
        model = area
        fields = "__all__"