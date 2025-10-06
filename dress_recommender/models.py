from django.db import models
from django.conf import settings
from store.models import Product

class WeatherData(models.Model):
    """Model to store weather information"""
    city = models.CharField(max_length=100, default='New York')
    temperature = models.FloatField()  # in Celsius
    condition = models.CharField(max_length=50)  # sunny, rainy, cloudy, etc.
    humidity = models.IntegerField()  # percentage
    wind_speed = models.FloatField()  # km/h
    feels_like = models.FloatField()  # in Celsius
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.city} - {self.temperature}°C, {self.condition}"
    
    @property
    def temperature_fahrenheit(self):
        return (self.temperature * 9/5) + 32

class DressRecommendation(models.Model):
    """Model to store dress recommendations"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    weather_data = models.ForeignKey(WeatherData, on_delete=models.CASCADE)
    recommended_products = models.ManyToManyField(Product, blank=True)
    recommendation_text = models.TextField()
    style_tips = models.TextField(blank=True)
    color_suggestions = models.CharField(max_length=200, blank=True)
    fabric_suggestions = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Recommendation for {self.weather_data.condition} weather"

class WeatherOutfitRule(models.Model):
    """Model to define outfit rules based on weather conditions"""
    WEATHER_CONDITIONS = [
        ('sunny', 'Sunny'),
        ('cloudy', 'Cloudy'),
        ('rainy', 'Rainy'),
        ('snowy', 'Snowy'),
        ('windy', 'Windy'),
        ('foggy', 'Foggy'),
    ]
    
    TEMPERATURE_RANGES = [
        ('very_cold', 'Very Cold (< 0°C)'),
        ('cold', 'Cold (0-10°C)'),
        ('cool', 'Cool (10-20°C)'),
        ('mild', 'Mild (20-25°C)'),
        ('warm', 'Warm (25-30°C)'),
        ('hot', 'Hot (> 30°C)'),
    ]
    
    condition = models.CharField(max_length=20, choices=WEATHER_CONDITIONS)
    temperature_range = models.CharField(max_length=20, choices=TEMPERATURE_RANGES)
    recommended_categories = models.CharField(max_length=200)  # comma-separated
    recommended_colors = models.CharField(max_length=200, blank=True)
    recommended_fabrics = models.CharField(max_length=200, blank=True)
    style_advice = models.TextField()
    
    def __str__(self):
        return f"{self.get_condition_display()} + {self.get_temperature_range_display()}"