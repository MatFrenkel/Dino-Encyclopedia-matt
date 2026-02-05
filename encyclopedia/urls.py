"""
URL routing for the encyclopedia app.
Maps URLs to controllers (views).
"""
from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('guest-login/', views.guest_login_view, name='guest_login'),
    
    # Main app URLs
    path('', views.home_view, name='home'),
    path('home/', views.home_view, name='home_alt'),
    path('map/', views.map_view, name='map'),
    
    # Gallery URLs
    path('gallery/', views.gallery_list_view, name='gallery'),
    path('gallery/<int:dinosaur_id>/', views.dinosaur_detail_view, name='dinosaur_detail'),
    
    # Library URL
    path('library/', views.library_view, name='library'),
    
    # Profile URLs
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.profile_update_view, name='profile_update'),
    
    # Game URLs
    path('puzzleaurus/', views.puzzleaurus_view, name='puzzleaurus'),
    path('memodyn/', views.memodyn_view, name='memodyn'),
]
