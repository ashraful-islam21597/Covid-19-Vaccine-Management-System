from django.urls import path

from home.views import HomeView,complete, registration

urlpatterns=[
    path('',HomeView.as_view(),name="home"),
    path('registration/',registration,name="registration"),
    #path('registration/',registrationView.as_view(),name="registration"),
    path('<int:pk>/',complete.as_view(),name="complete"),
]