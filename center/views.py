from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, ListView

from center.forms import centerform, areaform
from center.models import center_name, area


class CreateCenter(LoginRequiredMixin,View):
    form_class = centerform
    initial = {'key': 'value'}
    template_name = 'center_form.html'
    login_url = 'login'
    model_name=center_name
    def get(self,request,*args,**kwargs):
        form = self.form_class(initial=self.initial)
        obj=area.objects.get(id=self.kwargs['pk'])
        return render(request, self.template_name, {'form':form,'obj':obj})
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        #obj=area.objects.get(id=self.kwargs['pk'])

        form.instance.area_name = area.objects.get(id=self.kwargs['pk'])
        form.instance.area_name=area.objects.get(id=self.kwargs['pk'])
        if form.is_valid():
            form.save(self)
            form.instance.available_dosses = form.instance.updated_dosses
            form.instance.num_of_dosses = form.instance.doss_per_day
            form.save()

            return HttpResponseRedirect('/')

        return render(request, self.template_name, {'form': form})

class arealist(ListView):
    model = area
    template_name = 'arealist.html'
class CreateArea(CreateView):
    # form_class = areaform
    model = area
    template_name = 'area_form.html'
    fields = "__all__"
    #login_url = 'home'
    success_url = '/'

    def form_valid(self, form):
        #form.instance.author = self.request.user
        return super().form_valid(form)
