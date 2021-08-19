from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView, DeleteView, UpdateView

from City.models import area
from center.forms import centerform
from center.models import center_name


class CreateCenter(LoginRequiredMixin, View):
    form_class = centerform
    initial = {'key': 'value'}
    template_name = 'center_form.html'
    login_url = 'login'
    model_name = center_name

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        obj = area.objects.get(id=self.kwargs['pk'])
        return render(request, self.template_name, {'form': form, 'obj': obj})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        form.instance.area_name = area.objects.get(id=self.kwargs['pk'])
        form.instance.area_name = area.objects.get(id=self.kwargs['pk'])
        if form.is_valid():
            form.save(self)
            form.instance.available_dosses = form.instance.updated_dosses
            form.instance.num_of_dosses = form.instance.doss_per_day
            form.save()
            obj = area.objects.get(id=self.kwargs['pk'])
            return HttpResponseRedirect('/area/' + str(obj.id))
        return render(request, self.template_name, {'form': form})


class CenterDeleteView(LoginRequiredMixin, DeleteView):
    model = center_name
    template_name = 'center_delete.html'
    login_url = 'login'

    def get_success_url(self):
        return reverse_lazy('create_center', kwargs={'pk': self.object.area_name_id})

class CenterUpdateView(LoginRequiredMixin,UpdateView):
    model = center_name
    fields = '__all__'
    template_name = 'center_edit.html'
    login_url = 'login'
    def get_success_url(self):
        return reverse_lazy('create_center', kwargs={'pk': self.object.area_name_id})
