from django.contrib import admin
from .models import WardrobeItem, Outfit, WardrobeStats

@admin.register(WardrobeItem)
class WardrobeItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'category', 'brand', 'color', 'size', 'source', 'times_worn', 'favorite', 'created_at']
    list_filter = ['category', 'source', 'season', 'favorite', 'created_at']
    search_fields = ['name', 'brand', 'color', 'tags', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'description', 'category', 'brand', 'color', 'size', 'image')
        }),
        ('Purchase Information', {
            'fields': ('source', 'store_product', 'purchase_date', 'purchase_price')
        }),
        ('Style & Usage', {
            'fields': ('season', 'tags', 'times_worn', 'last_worn', 'favorite')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(Outfit)
class OutfitAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'occasion', 'season', 'times_worn', 'favorite', 'created_at']
    list_filter = ['season', 'favorite', 'created_at']
    search_fields = ['name', 'occasion', 'user__username']
    filter_horizontal = ['items']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(WardrobeStats)
class WardrobeStatsAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_items', 'total_outfits', 'most_worn_category', 'total_value', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    
    def has_add_permission(self, request):
        return False  # Stats are auto-generated