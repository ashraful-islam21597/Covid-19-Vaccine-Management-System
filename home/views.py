import math

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, CreateView, TemplateView, DetailView
import datetime



from center.models import center_name, period_of_dosses
from home.forms import registrationForm
from user.models import user


class HomeView(ListView):
    model = center_name
    template_name = 'home.html'
# class registration(CreateView):
#     model = user
#
#     template_name = 'home.html'
#     fields = ('nid','center','periods',)
#
#
#     def form_valid(self, form):
#         #form.instance.center = self.request.center
#         #form.instance.periods = self.request.center
#         return super().form_valid(form)


# class registrationView(View):
#     form_class = registrationForm
#     initial = {'key': 'value'}
#     template_name = 'registration.html'
#     #login_url = 'login'
#     model_name=user
#
#
#     def get(self,request,*args,**kwargs):
#         form = self.form_class(initial=self.initial)
#         #obj=center_name.objects.get(id=self.kwargs['pk'])
#         return render(request, self.template_name, {'form':form})
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         #form.instance.center = self.request.name
#         #form.instance.article=center_name.objects.get(id=self.kwargs['pk'])
#         if form.is_valid():
#             form.save(self)
#
#             return HttpResponseRedirect('/welcome/')
#
#         return render(request, self.template_name, {'form': form})
class complete(DetailView):
    model = user
    template_name = "registration_complete.html"

def registration(request):
    obj=center_name.objects.all()
    obj_period=period_of_dosses.objects.all()
    if 'submit' in request.POST:
        u=""
        starttime = datetime.time(00, 00, 00)
        endtime = datetime.time(00, 00, 00)
        nid = request.POST['nid']
        center=request.POST['center']
        c=center_name.objects.get(name=center)
        x1=(c.updated_dosses//c.doss_per_day)-(math.ceil(c.available_dosses/c.doss_per_day))
        if 0<c.num_of_dosses<=2:
            starttime = datetime.time(12, 00, 00)
            endtime = datetime.time(13, 00, 00)
            u="D"
        elif 4>=c.num_of_dosses>2:
            starttime = datetime.time(11, 00, 00)
            endtime = datetime.time(12, 00, 00)
            u="C"
        elif 6>=c.num_of_dosses>4:
            starttime = datetime.time(10, 00, 00)
            endtime = datetime.time(11, 00, 00)
            u="B"
        elif c.num_of_dosses>6:
            starttime = datetime.time(9, 00, 00)
            endtime = datetime.time(10, 00, 00)
            u="A"
        p=period_of_dosses(slot=u,start_time=starttime,end_time=endtime,date=c.working_time+datetime.timedelta(days=x1))
        p.save()
        p.center_name.add(c)
        p.num_user+=1
        p.save()
        try:
            c.num_of_dosses-=1
            c.available_dosses-=1
            c.save()
            d=user(nid=nid,center_id=c.id,period_id=p.id)
            d.save()
            d1=user.objects.get(nid=d.nid)
            if c.num_of_dosses==0 and c.available_dosses>=c.doss_per_day:
                c.num_of_dosses=c.doss_per_day
                c.save()
            return HttpResponseRedirect(reverse('complete', args=(d1.pk,)))
        except:
            p.delete()
            c.num_of_dosses=c.num_of_dosses+1
            c.available_dosses=c.available_dosses+1
            c.save()
            return HttpResponse("nid exists")
    return render(request,'registration.html',context={
        'obj':obj,
        'obj_period':obj_period
    })
