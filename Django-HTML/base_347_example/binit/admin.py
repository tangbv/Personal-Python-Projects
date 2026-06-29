from django.contrib import admin
from .models import Category, Item, Game, GameItem, HighScore

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'correct_category')
    list_filter = ('correct_category',)

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'start_time', 'end_time', 'score')
    list_filter = ('user',)

@admin.register(GameItem)
class GameItemAdmin(admin.ModelAdmin):
    list_display = ('game', 'item', 'guessed_category', 'is_correct')
    list_filter = ('is_correct', 'guessed_category')

@admin.register(HighScore)
class HighScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'date_achieved')
    list_filter = ('user', 'score', 'date_achieved')
    search_fields = ('user__username',)