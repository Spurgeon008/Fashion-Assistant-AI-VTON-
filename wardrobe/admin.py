from django.contrib import admin
from .models import WardrobeItem

@admin.register(WardrobeItem)
class WardrobeItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'color', 'size', 'purchase_date', 'times_worn', 'favorite']
    list_filter = ['favorite', 'purchase_date']
    search_fields = ['user__email', 'product__product_name']
    readonly_fields = ['purchase_date']
