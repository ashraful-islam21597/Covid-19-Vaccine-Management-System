from django.urls import path

from home.views import HomepageView,testview
from home.views import HomeView




urlpatterns = [
    path('', HomepageView, name="homepage"),
    path('registration/', HomeView.as_view(), name="home"),
    path('vaccination/', testview.as_view(), name='test')

]
