"""
Business logic services for the encyclopedia app.
Separates business logic from views (controllers).
"""
from django.db.models import Q
from django.utils import timezone
from .models import Dinosaur, UserProfile, AlbumItem, Period, GameScore


def get_dinosaurs_by_period(period_name=None):
    """
    Get dinosaurs filtered by period.
    
    Args:
        period_name: Name of the geological period (optional)
    
    Returns:
        QuerySet of Dinosaur objects
    """
    if period_name:
        return Dinosaur.objects.filter(period__name=period_name).select_related('period')
    return Dinosaur.objects.all().select_related('period')


def get_dinosaurs_by_diet(diet):
    """
    Get dinosaurs filtered by diet type.
    
    Args:
        diet: Type of diet (herbivore, carnivore, omnivore)
    
    Returns:
        QuerySet of Dinosaur objects
    """
    return Dinosaur.objects.filter(diet=diet).select_related('period')


def search_dinosaurs(query):
    """
    Search dinosaurs by name or scientific name.
    
    Args:
        query: Search query string
    
    Returns:
        QuerySet of matching Dinosaur objects
    """
    return Dinosaur.objects.filter(
        Q(name__icontains=query) | Q(scientific_name__icontains=query)
    ).select_related('period')


def get_user_progress(user):
    """
    Calculate user's album completion progress.
    
    Args:
        user: User object
    
    Returns:
        Dictionary with progress data
    """
    total_dinosaurs = Dinosaur.objects.count()
    collected = AlbumItem.objects.filter(user=user, is_collected=True).count()
    
    progress_percentage = 0
    if total_dinosaurs > 0:
        progress_percentage = round((collected / total_dinosaurs) * 100, 2)
    
    return {
        'total': total_dinosaurs,
        'collected': collected,
        'remaining': total_dinosaurs - collected,
        'percentage': progress_percentage
    }


def update_user_tokens(user, amount):
    """
    Update user's token count.
    
    Args:
        user: User object
        amount: Amount to add (positive) or subtract (negative)
    
    Returns:
        Updated token count
    """
    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.tokens += amount
    if profile.tokens < 0:
        profile.tokens = 0
    profile.save()
    return profile.tokens


def collect_dinosaur(user, dinosaur):
    """
    Mark a dinosaur as collected in user's album.
    
    Args:
        user: User object
        dinosaur: Dinosaur object
    
    Returns:
        AlbumItem object
    """
    album_item, created = AlbumItem.objects.get_or_create(
        user=user,
        dinosaur=dinosaur
    )
    
    if not album_item.is_collected:
        album_item.is_collected = True
        album_item.collected_at = timezone.now()
        album_item.save()
        
        # Award tokens for new discovery
        update_user_tokens(user, 10)
    
    return album_item


def check_album_completion(user):
    """
    Check if user has completed their album.
    
    Args:
        user: User object
    
    Returns:
        Boolean indicating completion status
    """
    progress = get_user_progress(user)
    return progress['percentage'] >= 100


def get_map_data():
    """
    Prepare geological period data for map view.
    
    Returns:
        QuerySet of Period objects with dinosaur counts
    """
    periods = Period.objects.all()
    map_data = []
    
    for period in periods:
        map_data.append({
            'period': period,
            'dinosaur_count': period.dinosaurs.count()
        })
    
    return map_data


def save_game_score(user, game_type, score):
    """
    Save a game score for a user.
    
    Args:
        user: User object
        game_type: Type of game ('puzzleaurus' or 'memodyn')
        score: Score achieved
    
    Returns:
        GameScore object
    """
    game_score = GameScore.objects.create(
        user=user,
        game_type=game_type,
        score=score
    )
    
    # Award tokens based on score
    token_award = max(1, score // 10)
    update_user_tokens(user, token_award)
    
    return game_score


def get_user_high_scores(user, game_type=None):
    """
    Get user's high scores.
    
    Args:
        user: User object
        game_type: Optional game type filter
    
    Returns:
        QuerySet of GameScore objects
    """
    scores = GameScore.objects.filter(user=user)
    if game_type:
        scores = scores.filter(game_type=game_type)
    return scores.order_by('-score')[:10]


def get_or_create_user_profile(user):
    """
    Get or create user profile.
    
    Args:
        user: User object
    
    Returns:
        UserProfile object
    """
    profile, created = UserProfile.objects.get_or_create(user=user)
    return profile
