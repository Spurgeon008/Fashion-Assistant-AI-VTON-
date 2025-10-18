from django.urls import path
from . import views
from .views_weather import weather_recommendations

urlpatterns=[
    path('',views.store,name='store'),
    path('category/<slug:category_slug>/',views.store,name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/',views.product_detail,name='product_detail'),
    path('search/',views.search,name='search'),
    path('weather-style/',weather_recommendations,name='weather_recommendations'),
]