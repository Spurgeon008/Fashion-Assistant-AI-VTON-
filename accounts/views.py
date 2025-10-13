from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .models import Account

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        phone_number = request.POST.get('phone_number', '')
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        # Validation
        if password == confirm_password:
            if Account.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists!')
                return redirect('register')
            elif Account.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists!')
                return redirect('register')
            else:
                # Create user
                user = Account.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    username=username,
                    password=password
                )
                user.phone_number = phone_number
                user.save()
                
                messages.success(request, 'Registration successful! You can now sign in.')
                return redirect('signin')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')
    
    return render(request, 'accounts/register.html')

def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials!')
            return redirect('signin')
    
    return render(request, 'accounts/signin.html')

@login_required(login_url='signin')
def signout(request):
    auth.logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('signin')

@login_required(login_url='signin')
def profile(request):
    user = request.user
    
    if request.method == 'POST':
        # Update basic info
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        user.address_line_1 = request.POST.get('address_line_1', user.address_line_1)
        user.address_line_2 = request.POST.get('address_line_2', user.address_line_2)
        user.city = request.POST.get('city', user.city)
        user.state = request.POST.get('state', user.state)
        user.country = request.POST.get('country', user.country)
        user.postal_code = request.POST.get('postal_code', user.postal_code)
        
        # Handle image uploads
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        if 'face_image' in request.FILES:
            user.face_image = request.FILES['face_image']
        if 'upper_body_image' in request.FILES:
            user.upper_body_image = request.FILES['upper_body_image']
        if 'full_body_image' in request.FILES:
            user.full_body_image = request.FILES['full_body_image']
        
        user.save()
        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('profile')
    
    context = {
        'user': user,
    }
    return render(request, 'accounts/profile.html', context)

@login_required(login_url='signin')
def edit_profile(request):
    return profile(request)
