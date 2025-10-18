from django.db import models
from django.conf import settings

class WardrobeItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wardrobe_items')
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE)
    color = models.CharField(max_length=50, blank=True)
    size = models.CharField(max_length=20, blank=True)
    purchase_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    times_worn = models.IntegerField(default=0)
    favorite = models.BooleanField(default=False)
    
    class Meta:
        app_label = 'wardrobe'
        ordering = ['-purchase_date']
        
    def __str__(self):
        return f"{self.user.email} - {self.product.product_name}"
