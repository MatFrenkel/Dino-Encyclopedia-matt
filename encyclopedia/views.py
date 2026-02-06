"""
Controllers (Django Views) for the encyclopedia app.
Following MVC pattern: these are the Controllers that coordinate between Models and Views (templates).
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from .models import Dinosaur, UserProfile, Period
from . import services


# ============= Authentication Controllers =============

def login_view(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'auth/login.html')


def register_view(request):
    """Handle user registration"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'auth/register.html')
        
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            # Create user profile
            services.get_or_create_user_profile(user)
            # Give welcome tokens
            services.update_user_tokens(user, 50)
            
            login(request, user)
            messages.success(request, f'Welcome to Dino Encyclopedia, {user.username}!')
            return redirect('home')
        except IntegrityError:
            messages.error(request, 'Username already exists.')
    
    return render(request, 'auth/register.html')


def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


def guest_login_view(request):
    """Handle guest login (creates temporary user)"""
    # Create or get guest user
    try:
        guest_user, created = User.objects.get_or_create(
            username='guest',
            defaults={'email': 'guest@example.com'}
        )
        if created:
            guest_user.set_password('guestpassword')
            guest_user.save()
            services.get_or_create_user_profile(guest_user)
    except IntegrityError:
        guest_user = User.objects.get(username='guest')
    
    login(request, guest_user)
    messages.info(request, 'Logged in as guest. Some features may be limited.')
    return redirect('home')


# ============= Main Application Controllers =============

@login_required
def home_view(request):
    """Home/Landing page controller"""
    profile = services.get_or_create_user_profile(request.user)
    progress = services.get_user_progress(request.user)
    
    context = {
        'user_profile': profile,
        'progress': progress,
    }
    return render(request, 'home.html', context)


@login_required
def map_view(request):
    """Map view controller showing geological periods"""
    map_data = services.get_map_data()
    
    # Ensure profile exists for the nav bar
    services.get_or_create_user_profile(request.user)
    
    context = {
        'map_data': map_data,
        'periods': Period.objects.all()
    }
    return render(request, 'map.html', context)


# ============= Gallery Controllers =============

@login_required
def gallery_list_view(request):
    """Gallery list controller with filtering"""
    # Get filter parameters
    period_filter = request.GET.get('period')
    diet_filter = request.GET.get('diet')
    search_query = request.GET.get('search')
    
    # Apply filters using services
    if search_query:
        dinosaurs = services.search_dinosaurs(search_query)
    elif diet_filter:
        dinosaurs = services.get_dinosaurs_by_diet(diet_filter)
    elif period_filter:
        dinosaurs = services.get_dinosaurs_by_period(period_filter)
    else:
        dinosaurs = services.get_dinosaurs_by_period()
    
    # Ensure profile exists for the nav bar
    services.get_or_create_user_profile(request.user)
    
    periods = Period.objects.all()
    
    context = {
        'dinosaurs': dinosaurs,
        'periods': periods,
        'current_period': period_filter,
        'current_diet': diet_filter,
        'search_query': search_query,
    }
    return render(request, 'gallery/list.html', context)


@login_required
def dinosaur_detail_view(request, dinosaur_id):
    """Dinosaur detail controller"""
    dinosaur = get_object_or_404(Dinosaur, id=dinosaur_id)
    
    # Collect dinosaur if not already collected
    if request.method == 'POST' and 'collect' in request.POST:
        services.collect_dinosaur(request.user, dinosaur)
        messages.success(request, f'{dinosaur.name} added to your collection!')
        return redirect('dinosaur_detail', dinosaur_id=dinosaur_id)
    
    # Ensure profile exists
    services.get_or_create_user_profile(request.user)
    
    context = {
        'dinosaur': dinosaur,
    }
    return render(request, 'gallery/detail.html', context)


# ============= Library Controller =============

@login_required
def library_view(request):
    """Library/educational content controller"""
    # Ensure profile exists
    services.get_or_create_user_profile(request.user)
    
    periods = Period.objects.all()
    
    context = {
        'periods': periods,
    }
    return render(request, 'library.html', context)


# ============= Profile Controllers =============

@login_required
def profile_view(request):
    """User profile controller"""
    profile = services.get_or_create_user_profile(request.user)
    progress = services.get_user_progress(request.user)
    recent_scores = services.get_user_high_scores(request.user)
    
    context = {
        'user_profile': profile,
        'progress': progress,
        'recent_scores': recent_scores,
    }
    return render(request, 'profile.html', context)


@login_required
def profile_update_view(request):
    """Handle profile updates"""
    if request.method == 'POST':
        profile = services.get_or_create_user_profile(request.user)
        
        # Update user info
        request.user.email = request.POST.get('email', request.user.email)
        request.user.save()
        
        # Update avatar if uploaded
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
            profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return redirect('profile')


# ============= Game Controllers =============

@login_required
def puzzleaurus_view(request):
    """Puzzleaurus game controller"""
    if request.method == 'POST':
        score = int(request.POST.get('score', 0))
        services.save_game_score(request.user, 'puzzleaurus', score)
        messages.success(request, f'Score saved: {score} points! Tokens awarded.')
        return redirect('puzzleaurus')
    
    high_scores = services.get_user_high_scores(request.user, 'puzzleaurus')
    
    # Ensure profile exists
    services.get_or_create_user_profile(request.user)
    
    context = {
        'high_scores': high_scores,
    }
    return render(request, 'puzzleaurus.html', context)


@login_required
def memodyn_view(request):
    """Memodyn game controller"""
    if request.method == 'POST':
        score = int(request.POST.get('score', 0))
        services.save_game_score(request.user, 'memodyn', score)
        messages.success(request, f'Score saved: {score} points! Tokens awarded.')
        return redirect('home')
    
    high_scores = services.get_user_high_scores(request.user, 'memodyn')
    
    # Ensure profile exists
    services.get_or_create_user_profile(request.user)
    
    context = {
        'high_scores': high_scores,
    }
    return render(request, 'memodyn.html', context)
