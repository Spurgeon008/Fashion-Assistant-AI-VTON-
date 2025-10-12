from django.shortcuts import render
from store.models import Product

def home(request):
    products = Product.objects.all().filter(is_available=True)
    context={
        'products':products,
    }
    return render(request,'home.html',context)
    prompt = getattr(settings, 'VTON_DEFAULT_PROMPT', "Combine the subjects of these images in a natural way, producing a new image.")
