from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from City.models import area
from City.priority import priority
from center.forms import centerform
from center.models import center_name


class CreateCenter(LoginRequiredMixin, View):
    form_class = centerform
    initial = {'key': 'value'}
    template_name = 'admin/center/center_form.html'
    login_url = 'login'
    model_name = center_name

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        obj = area.objects.get(id=self.kwargs['pk'])
        # obj.enability=True
        # obj.save()
        # a=area.objects.all()
        # for i in a:
        #     if i.enability ==True:
        #         i.priority = priority(i.id)
        #         i.save()

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
            obj.number_of_center = obj.number_of_center + 1
            #obj.save()
            #obj = area.objects.get(id=self.kwargs['pk'])
            obj.enability=True
            obj.save()
            a=area.objects.all()
            for i in a:
                if i.enability ==True:
                    i.priority = priority(i.id)
                    i.save()
            return HttpResponseRedirect('/area/' + str(obj.id))
        return render(request, self.template_name, {'form': form})


class CenterDeleteView(LoginRequiredMixin, DeleteView):
    model = center_name
    template_name = 'admin/center/center_delete.html'
    login_url = 'login'

    def get_success_url(self):
        return reverse_lazy('create_center',
                            kwargs={'pk': self.object.area_name_id})


def centerupdate(request,pk):
    obj = center_name.objects.get(id=pk)
    if 'disable' in request.POST:
        obj = center_name.objects.get(id=pk)
        obj1=area.objects.get(center_name=obj.id)
        obj.status=False
        obj.save()
        obj1.number_of_center-=1
        obj1.save()
        return redirect('/areadetails/')
    elif 'enable' in request.POST:
        obj = center_name.objects.get(id=pk)
        obj1=area.objects.get(center_name=obj.id)
        obj.status=True
        obj.save()
        obj1.number_of_center+=1
        obj1.save()
        return redirect('/areadetails/')
    else:
        return render(request,
                      'admin/center/center_edit.html',
                      {'obj':obj})


