from django.urls import path
from . import views

urlpatterns = [
    path('generate_vton/', views.generate_vton, name='generate_vton'),
]