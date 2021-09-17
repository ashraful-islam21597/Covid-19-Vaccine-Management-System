import json
import bd as bd
import requests
from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from center.models import area


class HomeView(ListView):
    model = area
    template_name = 'home/home.html'


def HomepageView(request):
    context = requests.get('https://corona.lmao.ninja/v2/all?yesterday').json
    context1 = requests.get('https://corona.lmao.ninja/v2/countries/Bangladesh?yesterday&strict&query%20').json
    return render(request, 'home/homepage.html', {'context': context, "context1": context1})


class testview(TemplateView):
    template_name = 'admin/center/center.html'
