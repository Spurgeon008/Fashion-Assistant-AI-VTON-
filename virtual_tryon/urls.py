from django.urls import path
from . import views

urlpatterns = [
    path('generate_vton/', views.generate_vton, name='generate_vton'),
    path('generate_video_vton/', views.generate_video_vton, name='generate_video_vton'),
]