from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from staff.forms import CustomUserCreationForm
from staff.models import user


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    model = user
    template_name = "signup.html"
class stafflist(ListView):
    model = user
    template_name = 'staff/staffinfo.html'
