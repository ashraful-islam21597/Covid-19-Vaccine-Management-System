from django.urls import path

from home.views import testview
from home.views import HomeView

urlpatterns=[
    path('',HomeView.as_view(),name="home"),
    path('vaccination/',testview.as_view(),name='test')
    #path('registration/',registration,name="registration"),
    #path('<int:pk>/',complete.as_view(),name="complete"),
]