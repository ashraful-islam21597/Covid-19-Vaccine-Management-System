from django.forms import ModelForm

from center.models import center_name, area


class centerform(ModelForm):
    class Meta:
        model = center_name
        fields = ('name','updated_dosses','working_time','doss_per_day')
class areaform(ModelForm):
    class Meta:
        model = area
        fields = "__all__"