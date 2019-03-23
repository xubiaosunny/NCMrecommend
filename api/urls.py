from django.urls import path
from . import views


urlpatterns = [
    path('set_record/', views.set_record),
    path('get_record/', views.get_record),
    path('get_recommend/', views.get_recommend),
]
