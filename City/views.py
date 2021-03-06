import math
from math import floor
import bd as bd
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView, TemplateView

from City.models import area, dosses_for_dhaka
from City.priority import priority
from center.models import center_name
from citizen.models import Registration_pending
from citizen.registration import registration

x=(bd.thana)
y=x.get("Dhaka")
y1=y.get('Dhaka')

class arealist(ListView):
    model = area
    template_name = 'admin/area/arealist.html'




def createarea(request):
    a2 = area.objects.all()

    if 'submit' in request.POST:
        name = request.POST['name']
        population = request.POST['population']
        a = area(name=name,enability=False, population=population)
        a.save()
        # area1 = area.objects.all()
        # for i in area1:
        #     i.priority = priority(i.id)
        #     i.save()
        return redirect('/areadetails/')
    return render(request, 'admin/area/arealist.html', {'a2': a2,'y1':y1})


class areaDeleteView(LoginRequiredMixin, DeleteView):
    model = area
    template_name = 'admin/area/area_delete.html'
    login_url = 'login'
    success_url = reverse_lazy('arealist')


def updatedoss(request):
    if 'update' in request.POST:
        doss = request.POST['doss']
        d = dosses_for_dhaka(dosses=doss)
        d.save()
        a = area.objects.all()
        for i in a:

            if i.enability == True:
                # i.priority = priority(i.id)
                # i.save()
                i.pending_doss = round(float(d.dosses) * (i.priority / 100))
                i.total_doss_area = i.total_doss_area + round(float(d.dosses) * (i.priority / 100))
                i.save()
                center = i.center_name_set.all()
                f = i.pending_doss % i.number_of_center
                for c in center:
                    if f != 0:
                        c.pending_doss_center = c.pending_doss_center + round(i.pending_doss / i.number_of_center) + 1
                        f = f - 1
                    else:
                        if c.status == True:
                            c.pending_doss_center = c.pending_doss_center + round(i.pending_doss / i.number_of_center)
                    c.save()
                    c.total_doss_center = c.total_doss_center + c.pending_doss_center
                    c.save()
                    if c.updated_dosses == 0:
                        if c.status == True:
                            c.updated_dosses = c.pending_doss_center
                            c.available_dosses = c.pending_doss_center
                            if math.floor(c.updated_dosses / 7) % 4 == 0:
                                c.doss_per_day = math.floor(c.updated_dosses / 7)
                            else:
                                c.doss_per_day = math.floor(c.updated_dosses / 7) - (math.floor(c.updated_dosses / 7) % 4)

                            c.save()
                            c.num_of_dosses = c.doss_per_day
                            c.pending_doss_center = c.pending_doss_center - c.updated_dosses
                            c.save()

                            pending=Registration_pending.objects.all()
                            for j in pending:
                                if j.center.id==c.id:
                                    registration(c,j.id)
                                    #Registration_pending(c.id,j.nid)
                                    j.delete()


        return HttpResponseRedirect('/areadetails/')
    else:
        return render(request, 'admin/superuser/update_doss.html')
