from django.urls import path
from . import views

app_name = 'wardrobe'

urlpatterns = [
    # Dashboard
    path('', views.wardrobe_dashboard, name='dashboard'),
    
    # Items
    path('items/', views.wardrobe_items, name='items'),
    path('items/add/', views.add_manual_item, name='add_item'),
    path('items/<int:item_id>/', views.item_detail, name='item_detail'),
    path('items/<int:item_id>/edit/', views.edit_item, name='edit_item'),
    path('items/<int:item_id>/delete/', views.delete_item, name='delete_item'),
    path('items/<int:item_id>/toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('items/<int:item_id>/mark-worn/', views.mark_worn, name='mark_worn'),
    
    # Outfits
    path('outfits/', views.outfits_list, name='outfits'),
    path('outfits/create/', views.create_outfit, name='create_outfit'),
    path('outfits/generate/', views.generate_outfit_ai, name='generate_outfit'),
    path('outfits/save-ai/', views.save_ai_outfit, name='save_ai_outfit'),
    path('outfits/<int:outfit_id>/', views.outfit_detail, name='outfit_detail'),
]