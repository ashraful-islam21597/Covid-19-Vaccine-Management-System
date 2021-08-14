import math

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, CreateView, TemplateView, DetailView
import datetime

from center.counter import counter
from center.models import center_name, period_of_dosses, area
from home.forms import registrationForm
from citizen.models import people


class HomeView(ListView):
    model = area
    template_name = 'home.html'

class complete(DetailView):
    model = people
    template_name = "registration_complete.html"

def registration(request):
    obj=center_name.objects.all()
    obj_period=period_of_dosses.objects.all()
    if 'submit' in request.POST:
        nid = request.POST['nid']
        center=request.POST['center']
        c=center_name.objects.get(name=center)
        x1=(c.updated_dosses//c.doss_per_day)-(math.ceil(c.available_dosses/c.doss_per_day))
        if c.available_dosses==c.updated_dosses and c.updated_dosses%c.doss_per_day==1:
            c.num_of_dosses=c.doss_per_day+1
            c.save()
        slot_name,start,end=counter(c.doss_per_day,c.num_of_dosses,4)
        p=period_of_dosses(slot=slot_name,start_time=start,end_time=end,date=c.working_time+datetime.timedelta(days=x1))
        p.save()
        p.center_name.add(c)
        p.num_user+=1
        p.save()
        try:
            c.num_of_dosses-=1
            c.available_dosses-=1
            c.save()
            d=people(nid=nid,center_id=c.id,period_id=p.id)
            d.save()
            d1=people.objects.get(nid=d.nid)
            if c.num_of_dosses==0 and 0<c.available_dosses<=c.doss_per_day:
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
