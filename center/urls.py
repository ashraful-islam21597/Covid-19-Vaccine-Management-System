from django.urls import path

from center.views import CreateCenter, CreateArea, arealist

urlpatterns=[
    path('area/<int:pk>/',CreateCenter.as_view(), name="create_center"),
    path('area/', CreateArea.as_view(), name="create_area"),
    path('areadetails/', arealist.as_view(), name="arealist")
]