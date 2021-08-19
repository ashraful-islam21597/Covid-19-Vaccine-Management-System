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
class testview(TemplateView):
    template_name = 'center.html'

# x=area.objects.all()
# k=[]
# for i in x:
#     print(i.population-i.total_vaccinated)
#     k.append(i.population-i.total_vaccinated)
# p=(sum(k))
# print(k)
# print(p)
# priority=0
# k1=[]
# for i in k:
#     k1.append((i*100//p))
# print(k1)


