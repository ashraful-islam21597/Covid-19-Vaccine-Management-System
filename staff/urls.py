from django.urls import path

from staff.views import SignUpView, stafflist, center_staff_create, vaccinate

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('staffs/', stafflist.as_view(), name='staff'),
    path('center_staff/<int:pk>',center_staff_create, name='create_center_staff'),
    path('vaccinate/',vaccinate, name='vaccinate'),

]