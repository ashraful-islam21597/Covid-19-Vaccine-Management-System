from django.urls import path

from citizen.views import registration, complete

urlpatterns=[
    path('registration/',registration,name="registration"),
    path('<int:pk>/',complete.as_view(),name="complete"),
]