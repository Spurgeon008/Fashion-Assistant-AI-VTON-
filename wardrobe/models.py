from django.db import models
from django.conf import settings
from store.models import Product, Variation
from django.utils import timezone

class WardrobeItem(models.Model):
    CLOTHING_CATEGORIES = [
        ('tops', 'Tops'),
        ('bottoms', 'Bottoms'),
        ('dresses', 'Dresses'),
        ('outerwear', 'Outerwear'),
        ('shoes', 'Shoes'),
        ('accessories', 'Accessories'),
        ('activewear', 'Activewear'),
        ('formal', 'Formal Wear'),
        ('casual', 'Casual Wear'),
        ('other', 'Other'),
    ]
    
    SEASONS = [
        ('spring', 'Spring'),
        ('summer', 'Summer'),
        ('fall', 'Fall'),
        ('winter', 'Winter'),
        ('all_season', 'All Season'),
    ]
    
    SOURCE_CHOICES = [
        ('store_purchase', 'Purchased from Store'),
        ('manual_upload', 'Manually Added'),
        ('gift', 'Gift'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wardrobe_items')
    
    # Basic Information
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CLOTHING_CATEGORIES, default='other')
    brand = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    size = models.CharField(max_length=20, blank=True, null=True)
    
    # Images
    image = models.ImageField(upload_to='wardrobe/', blank=True, null=True)
    
    # Purchase Information
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='manual_upload')
    store_product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, 
                                    help_text="Link to store product if purchased from our store")
    purchase_date = models.DateField(blank=True, null=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Style Information
    season = models.CharField(max_length=20, choices=SEASONS, default='all_season')
    tags = models.CharField(max_length=500, blank=True, null=True, 
                          help_text="Comma-separated tags like 'casual, work, party'")
    
    # Usage Tracking
    times_worn = models.PositiveIntegerField(default=0)
    last_worn = models.DateField(blank=True, null=True)
    favorite = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.user.username}'s {self.name}"
    
    def get_tags_list(self):
        """Return tags as a list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        return []
    
    def mark_as_worn(self):
        """Mark item as worn today and increment counter"""
        self.times_worn += 1
        self.last_worn = timezone.now().date()
        self.save()

class Outfit(models.Model):
    """Model to store outfit combinations"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='outfits')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    items = models.ManyToManyField(WardrobeItem, related_name='outfits')
    
    # Occasion and Style
    occasion = models.CharField(max_length=100, blank=True, null=True)
    season = models.CharField(max_length=20, choices=WardrobeItem.SEASONS, default='all_season')
    
    # Usage
    times_worn = models.PositiveIntegerField(default=0)
    last_worn = models.DateField(blank=True, null=True)
    favorite = models.BooleanField(default=False)
    
    # Image of the complete outfit
    outfit_image = models.ImageField(upload_to='outfits/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.user.username}'s {self.name}"
    
    def mark_as_worn(self):
        """Mark outfit as worn and update all items"""
        self.times_worn += 1
        self.last_worn = timezone.now().date()
        self.save()
        
        # Mark all items in the outfit as worn
        for item in self.items.all():
            item.mark_as_worn()

class WardrobeStats(models.Model):
    """Model to track wardrobe statistics"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wardrobe_stats')
    total_items = models.PositiveIntegerField(default=0)
    total_outfits = models.PositiveIntegerField(default=0)
    most_worn_category = models.CharField(max_length=20, blank=True, null=True)
    favorite_season = models.CharField(max_length=20, blank=True, null=True)
    total_value = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Wardrobe Stats"
    
    def update_stats(self):
        """Update all statistics"""
        items = WardrobeItem.objects.filter(user=self.user)
        outfits = Outfit.objects.filter(user=self.user)
        
        self.total_items = items.count()
        self.total_outfits = outfits.count()
        
        # Calculate total value
        total_value = sum(item.purchase_price or 0 for item in items)
        self.total_value = total_value
        
        # Find most worn category
        if items.exists():
            category_counts = {}
            for item in items:
                category_counts[item.category] = category_counts.get(item.category, 0) + item.times_worn
            
            if category_counts:
                self.most_worn_category = max(category_counts, key=category_counts.get)
        
        self.save()