from django.urls import path
from . import views


urlpatterns = [
    path('set_record/', views.set_record),
    path('get_record/', views.get_record),
    path('add_music_collection/', views.add_music_collection),
    path('del_music_collection/', views.del_music_collection),
    path('get_music_collection/', views.get_music_collection),
    path('get_recommend/', views.get_recommend),
]
