from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

@login_required(login_url='signin')
def wardrobe(request):
    """Display user's wardrobe"""
    from .models import WardrobeItem
    wardrobe_items = WardrobeItem.objects.filter(user=request.user)
    
    context = {
        'wardrobe_items': wardrobe_items,
        'total_items': wardrobe_items.count(),
        'favorites': wardrobe_items.filter(favorite=True).count(),
    }
    return render(request, 'wardrobe/wardrobe.html', context)

@login_required(login_url='signin')
def add_to_wardrobe(request, product_id):
    """Add a product to user's wardrobe"""
    if request.method == 'POST':
        from store.models import Product
        from .models import WardrobeItem
        product = get_object_or_404(Product, id=product_id)
        color = request.POST.get('color', '')
        size = request.POST.get('size', '')
        notes = request.POST.get('notes', '')
        
        # Check if item already exists
        existing_item = WardrobeItem.objects.filter(
            user=request.user,
            product=product,
            color=color,
            size=size
        ).first()
        
        if existing_item:
            messages.info(request, 'This item is already in your wardrobe!')
        else:
            WardrobeItem.objects.create(
                user=request.user,
                product=product,
                color=color,
                size=size,
                notes=notes
            )
            messages.success(request, 'Item added to your wardrobe!')
        
        return redirect('wardrobe')
    
    return redirect('store')

@login_required(login_url='signin')
def remove_from_wardrobe(request, item_id):
    """Remove an item from wardrobe"""
    from .models import WardrobeItem
    item = get_object_or_404(WardrobeItem, id=item_id, user=request.user)
    item.delete()
    messages.success(request, 'Item removed from your wardrobe!')
    return redirect('wardrobe')

@login_required(login_url='signin')
def toggle_favorite(request, item_id):
    """Toggle favorite status of wardrobe item"""
    if request.method == 'POST':
        from .models import WardrobeItem
        item = get_object_or_404(WardrobeItem, id=item_id, user=request.user)
        item.favorite = not item.favorite
        item.save()
        return JsonResponse({'success': True, 'favorite': item.favorite})
    return JsonResponse({'success': False})

@login_required(login_url='signin')
def update_times_worn(request, item_id):
    """Update times worn counter"""
    if request.method == 'POST':
        from .models import WardrobeItem
        item = get_object_or_404(WardrobeItem, id=item_id, user=request.user)
        item.times_worn += 1
        item.save()
        return JsonResponse({'success': True, 'times_worn': item.times_worn})
    return JsonResponse({'success': False})

@login_required(login_url='signin')
def update_notes(request, item_id):
    """Update item notes"""
    if request.method == 'POST':
        from .models import WardrobeItem
        item = get_object_or_404(WardrobeItem, id=item_id, user=request.user)
        notes = request.POST.get('notes', '')
        item.notes = notes
        item.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
