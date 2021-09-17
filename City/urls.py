from django.urls import path

from City.views import arealist, createarea, areaDeleteView, updatedoss

urlpatterns = [
    path('areadetails/', createarea, name='arealist'),
    path('delete_area/<int:pk>', areaDeleteView.as_view(), name='delete_area'),
    path('update_doss/', updatedoss, name='update_doss'),

]
