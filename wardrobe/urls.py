from django.urls import path
from . import views

urlpatterns = [
    path('', views.wardrobe, name='wardrobe'),
    path('add/<int:product_id>/', views.add_to_wardrobe, name='add_to_wardrobe'),
    path('remove/<int:item_id>/', views.remove_from_wardrobe, name='remove_from_wardrobe'),
    path('toggle-favorite/<int:item_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('update-worn/<int:item_id>/', views.update_times_worn, name='update_times_worn'),
    path('update-notes/<int:item_id>/', views.update_notes, name='update_notes'),
]
