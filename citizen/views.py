import datetime
import math
import io

from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, UpdateView, TemplateView, DeleteView
from City.models import area
from City.priority import priority
from center.counter1 import counter1
from center.models import center_name, schedule
from citizen.models import people, Registration_pending

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.views.generic import View


# from citizen.utils import send_sms
from citizen.utils import send_sms


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


class PdfDownload(DetailView):
    def get(self, request, *args, **kwargs):
        template = get_template('user/vaccine_card.html')
        object = people.objects.get(id=self.kwargs['pk'])
        context = {
            'object': object

        }
        html = template.render(context)

        pdf = render_to_pdf('user/vaccine_card.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Vaccine_card_%s.pdf" % ("12341231")
            content = "Vaccine_card; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


class complete(DetailView):
    model = people
    template_name = "registration/registration_for_vaccine/registration_complete.html"
    # registration/registration_for_vaccine


class vaccine_status(DetailView):
    model = people
    template_name = "registration/status.html"
    # user/status.html


def check_status(request):
    if 'search' in request.POST:
        s = request.POST['s1']
        try:
            u = people.objects.get(nid=s)
            # if u.doss_1st==True:
            #     return HttpResponseRedirect(reverse('status', args=(u.pk,)))

            return HttpResponseRedirect(reverse('status', args=(u.pk,)))
        except:
            return render(request,
                          'invalid_nid.html', )
    context = {"nbar": "c"}
    return render(request, 'admin/center/center.html', context)


def download(request):
    if 'search' in request.POST:
        s = request.POST['s1']
        try:
            u = people.objects.get(nid=s)
            if u.doss_1st == True:
                return HttpResponseRedirect(reverse('complete', args=(u.pk,)))

            return HttpResponseRedirect(reverse('complete', args=(u.pk,)))
        except:
            return render(request,
                          'invalid_nid.html', )

    return render(request, 'admin/center/center.html')


class checkView(LoginRequiredMixin, UpdateView):
    model = people
    fields = ('registered', 'doss_1st')
    template_name = 'registration/registration_for_vaccine/vaccination_complete.html'
    login_url = 'login'

    def get_success_url(self):
        obj = people.objects.get(id=self.kwargs['pk'])
        obj1 = center_name.objects.get(name=obj.center)
        obj2 = area.objects.get(name=obj1.area_name)
        obj2.doss_1st_done += 1
        obj2.save()
        return reverse_lazy('vaccinate')


class second_doss_View(LoginRequiredMixin, UpdateView):
    model = people
    fields = ('registered', 'doss_2nd')
    template_name = 'registration/registration_for_vaccine/vaccination_complete.html'
    login_url = 'login'

    def get_success_url(self):
        obj = people.objects.get(id=self.kwargs['pk'])
        obj1 = center_name.objects.get(name=obj.center)
        obj2 = area.objects.get(name=obj1.area_name)
        obj2.total_vaccinated += 1
        obj2.save()
        return reverse_lazy('vaccinate')


def reg(request, pk):
    obj_period = schedule.objects.all()
    u = people.objects.get(id=pk)
    c = center_name.objects.get(id=u.center_id)
    obj1 = area.objects.get(name=c.area_name)
    obj = obj1.center_name_set.all()

    if 'submit' in request.POST:
        code = request.POST['code']
        if code == u.code.number:
            if c.available_dosses == 0 and c.pending_doss_center == 0:
                pending = Registration_pending(nid=u.nid, center_id=c.id, registered=False)
                pending.save()
                p = Registration_pending.objects.get(id=pending.pk)
                return HttpResponseRedirect(reverse('cancel_registration', args=(p.pk,)))
            else:
                try:
                    Registration_pending.objects.get(nid=u.nid)
                    return HttpResponse("Your registration is pending on another center")
                except:

                    x1 = (c.updated_dosses // c.doss_per_day) - (math.ceil(c.available_dosses / c.doss_per_day))
                    if x1 < 0:
                        x1 = c.updated_dosses // c.doss_per_day
                    if c.available_dosses == c.updated_dosses and c.updated_dosses % c.doss_per_day == 1:
                        c.num_of_dosses = c.doss_per_day + 1
                        c.save()
                    slot_name, start, end = counter1(c.doss_per_day, c.num_of_dosses, 4)
                    p = schedule(slot=slot_name, start_time=start, end_time=end,
                                 date=c.working_time + datetime.timedelta(days=x1),
                                 second_date=c.working_time + datetime.timedelta(days=x1 + 30))
                    p.save()
                    p.center_name.add(c)
                    p.num_user += 1
                    p.save()
                    try:
                        c.num_of_dosses -= 1
                        c.available_dosses -= 1
                        c.save()
                        u.registered = True
                        u.period_id = p.id
                        u.save()
                        m = area.objects.get(name=c.area_name)
                        m.total_rgistered += 1
                        m.save()
                        area1 = area.objects.all().filter(enability=True)
                        for i in area1:
                            print(priority(i.id))
                            i.priority = priority(i.id)

                            i.save()
                        d1 = people.objects.get(nid=u.nid)
                        if c.num_of_dosses == 0 and 0 < c.available_dosses > c.doss_per_day:
                            c.num_of_dosses = c.doss_per_day
                            c.save()
                        elif c.num_of_dosses == 0 and 0 < c.available_dosses <= c.doss_per_day:
                            c.num_of_dosses = c.available_dosses
                            c.save()
                        elif c.available_dosses == 0 and c.pending_doss_center != 0:
                            c.available_dosses = c.pending_doss_center
                            c.updated_dosses = c.pending_doss_center
                            c.pending_doss_center = c.pending_doss_center - c.updated_dosses
                            c.save()
                            if math.floor(c.updated_dosses / 7) % 4 == 0:
                                c.doss_per_day = math.floor(c.updated_dosses / 7)
                            else:
                                c.doss_per_day = math.floor(c.updated_dosses / 7) - (
                                            math.floor(c.updated_dosses / 7) % 4)

                            c.save()
                            c.num_of_dosses = c.doss_per_day
                            c.save()

                        return HttpResponseRedirect(reverse('complete', args=(d1.pk,)))
                    except:
                        p.delete()
                        c.num_of_dosses = c.num_of_dosses + 1
                        c.available_dosses = c.available_dosses + 1
                        c.save()
                        return render(request,
                                      'invalid_nid.html', )
    return render(request,
                  'registration/registration_for_vaccine/verify.html',
                  context={
                      'obj': obj,
                      'obj_period': obj_period
                  })


def registration(request, pk):
    obj1 = area.objects.get(id=pk)
    obj = obj1.center_name_set.all()
    obj_period = schedule.objects.all()
    if 'submit' in request.POST:
        nid = request.POST['nid']
        center = request.POST['center']
        phone = request.POST['phone']
        c = center_name.objects.get(name=center)
        r = people.objects.create(nid=nid, contact=phone, center_id=c.id, registered=False, vaccinated=False,
                                  doss_1st=False,
                                  doss_2nd=False)
        send_sms(r.code.number,r.contact)
        return HttpResponseRedirect(reverse('reg', args=(r.pk,)))

    return render(request,
                  'registration/registration_for_vaccine/registration.html',
                  context={
                      'obj': obj,
                      'obj_period': obj_period
                  })


def cancel_registration(request, pk):
    object = Registration_pending.objects.get(id=pk)
    a = object.center.area_name
    print(a)
    obj = area.objects.get(name=a)
    u = people.objects.get(nid=object.nid)
    u.registered = False
    u.save()
    if "submit" in request.POST:
        object.delete()
        u.delete()
        return redirect('/registration/' + str(obj.id))
    return render(request,
                  'registration/registration_for_vaccine/registration_complete.html',
                  context={
                      'object': object,
                  })

    # def get_success_url(self):
    #     return reverse_lazy('registration'
    #                         )
