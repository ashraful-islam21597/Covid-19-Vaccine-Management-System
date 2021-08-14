from django.urls import path

from staff.views import SignUpView, stafflist

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('staffs/', stafflist.as_view(), name='staff'),
]