from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse

from django.views.generic import CreateView, ListView

from citizen.models import people
from staff.forms import CustomUserCreationForm
from staff.models import user, center_staff


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    model = user
    template_name = "registration/staff_access/signup.html"


class stafflist(ListView):
    model = user
    template_name = 'admin/superuser/staffinfo.html'


def center_staff_create(request, pk):
    if request.method == 'POST':
        staff = center_staff(username=request.POST['username'],
                             password=request.POST['password'],
                             name=request.POST['name'],
                             staff_id=pk)
        staff.save()
        User = user.objects.create_user(username=request.POST['username'],
                                        password=request.POST['password'],
                                        Fullname=request.POST['name'],
                                        staff_user=request.POST['user'],
                                        is_staff=True, is_active=True, is_cnter_staff=True,
                                        )
        User.save()
        return HttpResponseRedirect('/')
    else:
        return render(request, 'admin/center/center_staff.html')


def vaccinate(request):
    u1=center_staff.objects.get(username=request.user.username)
    if 'search' in request.POST:
        s = request.POST['s1']
        try:
            u = people.objects.get(nid=s)
            u2 = center_staff.objects.get(username=request.user.username)

            if u2.staff.name == u.center.name:
                if u.doss_1st == True:
                    return HttpResponseRedirect(reverse('second', args=(u.pk,)))

                return HttpResponseRedirect(reverse('check', args=(u.pk,)))

            else:
                return HttpResponse(" user not in the center")

        except:
            return HttpResponse("user not exists")

    return render(request, 'admin/center/center.html',context={
        'u1':u1
    })
