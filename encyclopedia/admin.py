from django.contrib import admin
from .models import Period, Dinosaur, UserProfile, AlbumItem, GameScore


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ['name', 'era', 'start_mya', 'end_mya']
    list_filter = ['era']
    search_fields = ['name', 'description']


@admin.register(Dinosaur)
class DinosaurAdmin(admin.ModelAdmin):
    list_display = ['name', 'scientific_name', 'period', 'diet', 'length_meters', 'weight_kg']
    list_filter = ['period', 'diet']
    search_fields = ['name', 'scientific_name', 'description']
    list_per_page = 20


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'tokens', 'progress_percentage', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at', 'progress_percentage']


@admin.register(AlbumItem)
class AlbumItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'dinosaur', 'is_collected', 'collected_at']
    list_filter = ['is_collected', 'dinosaur__period']
    search_fields = ['user__username', 'dinosaur__name']


@admin.register(GameScore)
class GameScoreAdmin(admin.ModelAdmin):
    list_display = ['user', 'game_type', 'score', 'completed_at']
    list_filter = ['game_type', 'completed_at']
    search_fields = ['user__username']
    date_hierarchy = 'completed_at'
