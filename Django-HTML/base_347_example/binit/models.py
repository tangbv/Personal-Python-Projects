from django.db import models
from django.conf import settings

# Model to represent the categories of items in the game
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
# Model to represent the items in the game. Each item will 
# belong to a category and will have a name and description
class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    correct_category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# Model to track the game session
# This model will store the user's score and the time taken to complete the game
class Game(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"Game {self.id} by {self.user}"

# Model to track each item in the game to determine if the user guessed the correct category
class GameItem(models.Model):
    game = models.ForeignKey(Game, related_name='game_items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    guessed_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.item.name} in Game {self.game.id}"
    
class HighScore(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.IntegerField()
    date_achieved = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.score}"
