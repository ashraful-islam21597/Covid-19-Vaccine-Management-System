from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DetailView, ListView

from center.models import center_name
from citizen.models import people
from staff.forms import CustomUserCreationForm, Center_staff_form
from staff.models import user, center_staff


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    model = user
    template_name = "signup.html"


class stafflist(ListView):
    model = user
    template_name = 'staff/staffinfo.html'


# class Center_staff_createview(LoginRequiredMixin,CreateView):
#     form_class = Center_staff_form
#     initial = {'key': 'value'}
#     template_name = 'center_staff.html'
#     login_url = 'login'
#     model_name = center_staff
#     def get(self, request, *args, **kwargs):
#         form = self.form_class(initial=self.initial)
#         obj = center_name.objects.get(id=self.kwargs['pk'])
#         return render(request, self.template_name, {'form': form, 'obj': obj})
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         form.instance.username = self.request.user
#         form.instance.article=Article.objects.get(id=self.kwargs['pk'])
#         if form.is_valid():
#             form.save(self)
#
#             return HttpResponseRedirect('/articles/')
#
#         return render(request, self.template_name, {'form': form})

def center_staff_create(request,pk):

    if request.method == 'POST':
        # username=request.POST['username']
        # password=request.POST['username']
        # name=request.POST['name']
        # staff_status=request.POST['status']
        # staff_user=request.POST['user']
        #x=center_name.objects.get(id=pk)
        staff=center_staff(username=request.POST['username'],
                           password=request.POST['password'],
                           name=request.POST['name'],
                           staff_id=pk)
        staff.save()
        User=user.objects.create_user(username=request.POST['username'],
                                 password=request.POST['password'],
                                 Fullname=request.POST['name'],
                                 staff_user=request.POST['user'],
                                 is_staff=True,is_active=True,is_cnter_staff=True,
                                 )
        User.save()
        return HttpResponseRedirect('/')
    else:
        return render(request, 'center_staff.html')

# def center_staff_create(request,pk):
#     if request.method == 'POST':
#         form = Center_staff_form(request.POST)
#         if form.is_valid():
#
#             form.save()
#             User=user.objects.create_user(username=form.instance.username,
#                                              password=form.instance.password,
#                                              Fullname=form.instance.name,
#                                              staff_user=request.POST['user'],
#                                              is_staff=True,is_active=True,is_cnter_staff=True,
#                                              )
#             User.save()
#             return HttpResponseRedirect('/')
#
#
#     else:
#         form = Center_staff_form()
#
#     return render(request, 'center_staff.html', {'form': form})
def vaccinate(request):
    if 'search' in request.POST:
        s=request.POST['s1']
        try:
            u=people.objects.get(nid=s)
            u2=center_staff.objects.get(username=request.user.username)

            if u2.staff.name==u.center.name:
                if u.doss_1st==True:
                    return HttpResponseRedirect(reverse('second', args=(u.pk,)))

                return HttpResponseRedirect(reverse('check', args=(u.pk,)))

            else:
                return HttpResponse(" user not in the center")

        except:
            return HttpResponse("user not exists")

    return render(request,'center.html')



