from django.urls import path
from . import views

app_name = 'dress_recommender'

urlpatterns = [
    path('', views.dress_recommender_home, name='home'),
    path('recommend/', views.get_weather_recommendation, name='get_recommendation'),
    path('save/', views.save_recommendation, name='save_recommendation'),
    path('my-recommendations/', views.my_recommendations, name='my_recommendations'),
]