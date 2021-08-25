from django.urls import path

from citizen.views import registration, complete, PdfDownload, checkView, second_doss_View, check_status, \
    vaccine_status, download

urlpatterns=[
    path('registration/<int:pk>',registration,name="registration"),
    path('<int:pk>/',complete.as_view(),name="complete"),
    path('download/<int:pk>',PdfDownload.as_view(),name="download"),
    path('check/<int:pk>/',checkView.as_view(),name="check"),
    path('second_doss/<int:pk>/',second_doss_View.as_view(),name="second"),
    path('check_status/',check_status,name="check_status"),
    path('status/<int:pk>/',vaccine_status.as_view(),name="status"),
    path('download/',download,name="download"),
]