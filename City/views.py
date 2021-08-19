from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView, TemplateView

from City.models import area
from City.priority import priority


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


