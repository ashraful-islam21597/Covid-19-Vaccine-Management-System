import math
from math import floor

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView, TemplateView

from City.models import area, dosses_for_dhaka
from City.priority import priority
from center.models import center_name


class arealist(ListView):
    model = area
    template_name = 'arealist.html'


# class CreateArea(CreateView):
#     model = area
#     template_name = 'area_form.html'
#     fields = "__all__"
#     success_url = '/'
#
#     def form_valid(self, form):
#         return super().form_valid(form)
#     obj=area.objects.get(name=form.instance.name)
#     print(obj)

# class CreateArea(LoginRequiredMixin,View):
#     form_class = 'areaform'
#     initial = {'key': 'value'}
#     template_name = 'area_form.html'
#     login_url = 'login'
#     model_name=area
#
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         #form.instance.author = self.request.user
#         #form.instance.article=Article.objects.get(id=self.kwargs['pk'])
#         if form.is_valid():
#             form.save(self)
#             d1=area.objects.get(name=self.form.name)
#
#             return HttpResponseRedirect('/')
#             #return HttpResponseRedirect(reverse('area1', args=(d1.pk,)))
#
#         return render(request, self.template_name, {'form': form})
#     def area1(self,request,*args,**kwargs):
#         #form = self.form_class(initial=self.initial)
#         obj=area.objects.get(id=self.kwargs['pk'])
#         print(obj)
#         return HttpResponseRedirect('/')
#         #return render(request, self.template_name, {'form':form,'obj':obj})

def createarea(request):
    a2=area.objects.all()
    if 'submit' in request.POST:
        name=request.POST['name']
        population=request.POST['population']
        a=area(name=name,population=population)
        a.save()
        area1=area.objects.all()
        for i in area1:
            i.priority=priority(i.id)
            i.save()
        return redirect('/areadetails/')
    return render(request,'arealist.html',{'a2':a2})

class areaDeleteView(LoginRequiredMixin, DeleteView):
    model = area
    template_name = 'area_delete.html'
    login_url = 'login'
    success_url = reverse_lazy('arealist')


    # def get_success_url(self):
    #     return reverse_lazy('create_center', kwargs={'pk': self.object.area_name_id})
    #
def updatedoss(request):
    if 'update' in request.POST:
        doss=request.POST['doss']
        d=dosses_for_dhaka(dosses=doss)
        d.save()
        a=area.objects.all()
        for i in a:
            i.pending_doss=round(float(d.dosses)*(i.priority/100))
            i.total_doss_area=i.total_doss_area+round(float(d.dosses)*(i.priority/100))
            i.save()
            center=i.center_name_set.all()
            if i.number_of_center!=0:
                f=i.pending_doss%i.number_of_center
            for c in center:
                if f!=0:
                    c.pending_doss_center=c.pending_doss_center+round(i.pending_doss/i.number_of_center)+1
                    f=f-1
                else:
                    c.pending_doss_center=c.pending_doss_center+round(i.pending_doss/i.number_of_center)
                c.save()
                c.total_doss_center=c.total_doss_center+c.pending_doss_center
                c.save()
                if c.updated_dosses==0:
                    c.updated_dosses=c.pending_doss_center
                    c.available_dosses=c.pending_doss_center
                    if math.floor(c.updated_dosses / 7) % 4 == 0:
                        c.doss_per_day = math.floor(c.updated_dosses / 7)
                    else:
                        c.doss_per_day = math.floor(c.updated_dosses / 7) - (math.floor(c.updated_dosses / 7) % 4)
                    #c.doss_per_day=floor(c.pending_doss_center/7)
                    c.save()
                    c.num_of_dosses=c.doss_per_day
                    c.pending_doss_center=c.pending_doss_center-c.updated_dosses
                    c.save()

        return HttpResponseRedirect('/')
    else:
        return render(request,'update_doss.html')





