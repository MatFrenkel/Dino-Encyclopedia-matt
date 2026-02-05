from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Period(models.Model):
    """Geological period model"""
    ERA_CHOICES = [
        ('mesozoic', 'Mesozoic'),
    ]
    
    PERIOD_CHOICES = [
        ('triassic', 'Triassic'),
        ('jurassic', 'Jurassic'),
        ('cretaceous', 'Cretaceous'),
    ]
    
    name = models.CharField(max_length=100, choices=PERIOD_CHOICES, unique=True)
    era = models.CharField(max_length=100, choices=ERA_CHOICES, default='mesozoic')
    start_mya = models.IntegerField(help_text="Million years ago (start)")
    end_mya = models.IntegerField(help_text="Million years ago (end)")
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-start_mya']
    
    def __str__(self):
        return self.get_name_display()


class Dinosaur(models.Model):
    """Dinosaur model representing individual dinosaur species"""
    DIET_CHOICES = [
        ('herbivore', 'Herbivore'),
        ('carnivore', 'Carnivore'),
        ('omnivore', 'Omnivore'),
    ]
    
    name = models.CharField(max_length=200)
    scientific_name = models.CharField(max_length=200, blank=True)
    period = models.ForeignKey(Period, on_delete=models.CASCADE, related_name='dinosaurs')
    diet = models.CharField(max_length=20, choices=DIET_CHOICES)
    length_meters = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0.1)],
        help_text="Length in meters"
    )
    weight_kg = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.1)],
        help_text="Weight in kilograms"
    )
    description = models.TextField()
    fun_fact = models.TextField(blank=True)
    image = models.ImageField(upload_to='dinosaurs/', blank=True, null=True)
    discovered_year = models.IntegerField(
        blank=True, 
        null=True,
        validators=[MinValueValidator(1800), MaxValueValidator(2100)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """Extended user profile with game-specific data"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    tokens = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"
    
    @property
    def progress_percentage(self):
        """Calculate user's album completion percentage"""
        total_dinosaurs = Dinosaur.objects.count()
        if total_dinosaurs == 0:
            return 0
        collected = AlbumItem.objects.filter(user=self.user, is_collected=True).count()
        return round((collected / total_dinosaurs) * 100, 2)


class AlbumItem(models.Model):
    """Represents a dinosaur collection item in user's album"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='album_items')
    dinosaur = models.ForeignKey(Dinosaur, on_delete=models.CASCADE)
    is_collected = models.BooleanField(default=False)
    collected_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['user', 'dinosaur']
        ordering = ['dinosaur__period', 'dinosaur__name']
    
    def __str__(self):
        status = "✓" if self.is_collected else "✗"
        return f"{status} {self.user.username} - {self.dinosaur.name}"


class GameScore(models.Model):
    """Stores game scores for mini-games"""
    GAME_TYPES = [
        ('puzzleaurus', 'Puzzleaurus'),
        ('memodyn', 'Memodyn'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_scores')
    game_type = models.CharField(max_length=20, choices=GAME_TYPES)
    score = models.IntegerField(validators=[MinValueValidator(0)])
    completed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-completed_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_game_type_display()}: {self.score}"
