from django.urls import path

from City.views import arealist, createarea, areaDeleteView

urlpatterns = [
    # path('area/<int:pk>/', CreateCenter.as_view(), name="create_center"),
    #path('area/', CreateArea.as_view(), name="create_area"),
    #path('areadetails/', arealist.as_view(), name="arealist"),
    path('areadetails/',createarea,name='arealist'),
    path('delete_area/<int:pk>',areaDeleteView.as_view(),name='delete_area'),

]