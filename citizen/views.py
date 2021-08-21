import datetime
import math
from twilio.rest import Client
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView
from City.models import area
from City.priority import priority
from center.counter1 import counter1
from center.models import center_name, period_of_dosses
from citizen.models import people


class complete(DetailView):
    model = people
    template_name = "registration_complete.html"

# def get_center(request):
#     obj = center_name.objects.all()
#     return HttpResponseRedirect(reverse('complete', args=(d1.pk,)))


def registration(request,pk):
    obj1 = area.objects.get(id=pk)
    obj  = obj1.center_name_set.all()

    obj_period = period_of_dosses.objects.all()

    if 'submit' in request.POST:
        nid = request.POST['nid']
        center = request.POST['center']
        c = center_name.objects.get(name=center)

        # client = Client('AC961eb8256addcabce6da96cf3ebd2b54', 'c21de0267000c910be5344ffbe85f6f4')
        # verify = client.verify.services('1234')
        # verify.verifications.create(to='01954773688', channel='sms')

        x1 = (c.updated_dosses // c.doss_per_day) - (math.ceil(c.available_dosses / c.doss_per_day))
        if x1 < 0:
            x1 = c.updated_dosses // c.doss_per_day
        if c.available_dosses == c.updated_dosses and c.updated_dosses % c.doss_per_day == 1:
            c.num_of_dosses = c.doss_per_day + 1
            c.save()
        slot_name, start, end = counter1(c.doss_per_day, c.num_of_dosses, 4)
        p = period_of_dosses(slot=slot_name, start_time=start, end_time=end,
                             date=c.working_time + datetime.timedelta(days=x1))
        p.save()
        p.center_name.add(c)
        p.num_user += 1
        p.save()
        try:

            c.num_of_dosses -= 1
            c.available_dosses -= 1
            c.save()
            d = people(nid=nid, center_id=c.id, period_id=p.id, registered=True, vaccinated=False, doss_1st=False,
                       doss_2nd=False)
            d.save()
            m = area.objects.get(name=c.area_name)

            m.total_rgistered += 1

            m.save()
            area1 = area.objects.all()
            for i in area1:
                print(priority(i.id))
                i.priority = priority(i.id)
                print(i.id)
                i.save()
            d1 = people.objects.get(nid=d.nid)
            if c.num_of_dosses == 0 and 0 < c.available_dosses > c.doss_per_day:
                c.num_of_dosses = c.doss_per_day
                c.save()
            elif c.num_of_dosses == 0 and 0 < c.available_dosses <= c.doss_per_day:
                c.num_of_dosses = c.available_dosses
                c.save()
            elif c.available_dosses==0 and c.pending_doss_center!=0:
                c.available_dosses=c.pending_doss_center
                c.updated_dosses=c.pending_doss_center
                c.pending_doss_center=c.pending_doss_center-c.updated_dosses
                c.save()
                if math.floor(c.updated_dosses / 7)%2==0:
                    c.doss_per_day= math.floor(c.updated_dosses / 7)
                else:
                    c.doss_per_day= math.floor(c.updated_dosses / 7)+1

                c.save()
                c.num_of_dosses=c.doss_per_day
                c.save()

            return HttpResponseRedirect(reverse('complete', args=(d1.pk,)))
        except:
            p.delete()
            c.num_of_dosses = c.num_of_dosses + 1
            c.available_dosses = c.available_dosses + 1
            c.save()
            return HttpResponse("nid exists")
    return render(request, 'registration.html', context={
        'obj': obj,
        'obj_period': obj_period
    })
