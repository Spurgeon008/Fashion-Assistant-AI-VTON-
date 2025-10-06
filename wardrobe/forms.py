from django import forms
from .models import WardrobeItem, Outfit

class WardrobeItemForm(forms.ModelForm):
    class Meta:
        model = WardrobeItem
        fields = [
            'name', 'description', 'category', 'brand', 'color', 'size',
            'image', 'season', 'tags', 'purchase_date', 'purchase_price', 'favorite'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Item name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description (optional)'
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brand (optional)'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Color'
            }),
            'size': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Size'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'season': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tags (comma-separated, e.g., casual, work, party)'
            }),
            'purchase_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'purchase_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'favorite': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ManualItemForm(forms.ModelForm):
    """Simplified form for manually adding items"""
    class Meta:
        model = WardrobeItem
        fields = [
            'name', 'description', 'category', 'brand', 'color', 'size',
            'image', 'season', 'tags', 'purchase_date', 'purchase_price'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'What is this item called?',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Tell us more about this item...'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'brand': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brand name'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Primary color'
            }),
            'size': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Size (S, M, L, XL, etc.)'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'required': True
            }),
            'season': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'casual, work, party, formal, etc.'
            }),
            'purchase_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'purchase_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'How much did it cost?'
            }),
        }

class OutfitForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['items'].queryset = WardrobeItem.objects.filter(user=user)
            self.fields['items'].widget = forms.CheckboxSelectMultiple()
    
    class Meta:
        model = Outfit
        fields = ['name', 'description', 'items', 'occasion', 'season', 'outfit_image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Outfit name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe this outfit...'
            }),
            'occasion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'When would you wear this? (e.g., work, date night, casual)'
            }),
            'season': forms.Select(attrs={'class': 'form-control'}),
            'outfit_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }

class QuickAddForm(forms.Form):
    """Quick form for adding items from store purchases"""
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    add_to_wardrobe = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )