import datetime
import math
import io

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse
from django.template.loader import get_template
from reportlab.pdfgen import canvas
from twilio.rest import Client
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, UpdateView
from City.models import area
from City.priority import priority
from center.counter1 import counter1
from center.models import center_name, period_of_dosses
from citizen.models import people

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.views.generic import View


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    #p = canvas.Canvas(result)
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    # p.drawString(100, 100, "Hello world.")
    # p.showPage()
    # p.save()
    # result.seek(0)
    #pdf.drawString(100, 100, "Hello world.")
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


class PdfDownload(DetailView):
    def get(self, request, *args, **kwargs):
        template = get_template('vaccine_card.html')
        object = people.objects.get(id=self.kwargs['pk'])
        context = {
            'object': object

        }
        html = template.render(context)

        pdf = render_to_pdf('vaccine_card.html', context)
        # p = canvas.Canvas(pdf)
        # p.drawString(100, 100)
        # p.showPage()
        # p.save()


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
    template_name = "registration_complete.html"
class vaccine_status(DetailView):
    model = people
    template_name = "citizen/status.html"


def check_status(request):
    if 'search' in request.POST:
        s=request.POST['s1']
        try:
            u=people.objects.get(nid=s)
            # if u.doss_1st==True:
            #     return HttpResponseRedirect(reverse('status', args=(u.pk,)))

            return HttpResponseRedirect(reverse('status', args=(u.pk,)))
        except:
            return HttpResponse("user not exists")

    return render(request,'center.html')

def download(request):
    if 'search' in request.POST:
        s=request.POST['s1']
        try:
            u=people.objects.get(nid=s)
            if u.doss_1st==True:
                return HttpResponseRedirect(reverse('complete', args=(u.pk,)))

            return HttpResponseRedirect(reverse('complete', args=(u.pk,)))
        except:
            return HttpResponse("user not exists")

    return render(request,'center.html')



class checkView(LoginRequiredMixin, UpdateView):
    model = people
    fields = ('registered', 'doss_1st')
    template_name = 'people_edit.html'
    login_url = 'login'
    # def get(self,request,*args,**kwargs):
    #     #form = self.form_class(initial=self.initial)
    #     obj=people.objects.get(id=self.kwargs['pk'])
    #     obj1=center_name.objects.get(name=obj.center)
    #     print(obj1)
    #
    #     return render(request, self.template_name)
    def get_success_url(self):
        obj=people.objects.get(id=self.kwargs['pk'])
        obj1=center_name.objects.get(name=obj.center)
        obj2=area.objects.get(name=obj1.area_name)
        obj2.doss_1st_done +=1
        obj2.save()
        return reverse_lazy('vaccinate')


class second_doss_View(LoginRequiredMixin, UpdateView):
    model = people
    fields = ('registered', 'doss_2nd')
    template_name = 'people_edit.html'
    login_url = 'login'

    def get_success_url(self):
        obj=people.objects.get(id=self.kwargs['pk'])
        obj1=center_name.objects.get(name=obj.center)
        obj2=area.objects.get(name=obj1.area_name)
        obj2.total_vaccinated+=1
        obj2.save()
        return reverse_lazy('vaccinate')


def registration(request, pk):
    obj1 = area.objects.get(id=pk)
    obj = obj1.center_name_set.all()

    obj_period = period_of_dosses.objects.all()

    if 'submit' in request.POST:
        nid = request.POST['nid']
        center = request.POST['center']
        c = center_name.objects.get(name=center)
        x1 = (c.updated_dosses // c.doss_per_day) - (math.ceil(c.available_dosses / c.doss_per_day))
        if x1 < 0:
            x1 = c.updated_dosses // c.doss_per_day
        if c.available_dosses == c.updated_dosses and c.updated_dosses % c.doss_per_day == 1:
            c.num_of_dosses = c.doss_per_day + 1
            c.save()
        slot_name, start, end = counter1(c.doss_per_day, c.num_of_dosses, 4)
        p = period_of_dosses(slot=slot_name, start_time=start, end_time=end,
                             date=c.working_time + datetime.timedelta(days=x1),
                             second_date=c.working_time + datetime.timedelta(days=x1+30))
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
            elif c.available_dosses == 0 and c.pending_doss_center != 0:
                c.available_dosses = c.pending_doss_center
                c.updated_dosses = c.pending_doss_center
                c.pending_doss_center = c.pending_doss_center - c.updated_dosses
                c.save()
                if math.floor(c.updated_dosses / 7) % 4 == 0:
                    c.doss_per_day = math.floor(c.updated_dosses / 7)
                else:
                    c.doss_per_day = math.floor(c.updated_dosses / 7) - (math.floor(c.updated_dosses / 7) % 4)

                c.save()
                c.num_of_dosses = c.doss_per_day
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
