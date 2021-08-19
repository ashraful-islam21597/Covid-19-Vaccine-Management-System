from django.urls import path

from center.views import CreateCenter, CenterDeleteView, CenterUpdateView

urlpatterns = [
    path('area/<int:pk>/', CreateCenter.as_view(), name="create_center"),
    path('center/<int:pk>/', CenterDeleteView.as_view(), name="delete_center"),
    path('edit/center/<int:pk>/', CenterUpdateView.as_view(), name="edit_center"),
    # path('area/', CreateArea.as_view(), name="create_area"),
    # path('areadetails/', arealist.as_view(), name="arealist")
]
