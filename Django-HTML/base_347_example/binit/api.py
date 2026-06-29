from ninja import NinjaAPI, ModelSchema
from ninja.errors import HttpError
from .models import Game, GameItem, HighScore, Category, Item

api = NinjaAPI()

# Define schemas for your models
class GameSchema(ModelSchema):
    class Config:
        model = Game
        model_fields = ["id", "user", "start_time", "end_time", "score"]

class GameCreateSchema(ModelSchema):
    class Config:
        model = Game
        model_fields = ["user", "score"]

class GameUpdateSchema(ModelSchema):
    class Config:
        model = Game
        model_fields = ["end_time", "score"]

class CategorySchema(ModelSchema):
    class Config:
        model = Category
        model_fields = ["id", "name", "description"]

class ItemSchema(ModelSchema):
    class Config:
        model = Item
        model_fields = ["id", "name", "description", "correct_category"]

class GameItemSchema(ModelSchema):
    class Config:
        model = GameItem
        model_fields = ["id", "game", "item", "guessed_category", "is_correct"]

class HighScoreSchema(ModelSchema):
    class Config:
        model = HighScore
        model_fields = ["id", "user", "score", "date_achieved"]

# CRUD Endpoints for Game
@api.post("/games", response=GameSchema)
def create_game(request, payload: GameCreateSchema):
    game = Game.objects.create(**payload.dict())
    return game

@api.get("/games/{game_id}", response=GameSchema)
def retrieve_game(request, game_id: int):
    try:
        return Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        raise HttpError(404, f"Game with id {game_id} not found")

@api.put("/games/{game_id}", response=GameSchema)
def update_game(request, game_id: int, payload: GameUpdateSchema):
    try:
        game = Game.objects.get(id=game_id)
        for attr, value in payload.dict().items():
            setattr(game, attr, value)
        game.save()
        return game
    except Game.DoesNotExist:
        raise HttpError(404, f"Game with id {game_id} not found")

@api.delete("/games/{game_id}", response=dict)
def delete_game(request, game_id: int):
    try:
        game = Game.objects.get(id=game_id)
        game.delete()
        return {"success": True}
    except Game.DoesNotExist:
        raise HttpError(404, f"Game with id {game_id} not found")

# CRUD Endpoints for Category
@api.post("/categories", response=CategorySchema)
def create_category(request, payload: CategorySchema):
    category = Category.objects.create(**payload.dict())
    return category

@api.get("/categories/{category_id}", response=CategorySchema)
def retrieve_category(request, category_id: int):
    try:
        return Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        raise HttpError(404, f"Category with id {category_id} not found")

@api.put("/categories/{category_id}", response=CategorySchema)
def update_category(request, category_id: int, payload: CategorySchema):
    try:
        category = Category.objects.get(id=category_id)
        for attr, value in payload.dict().items():
            setattr(category, attr, value)
        category.save()
        return category
    except Category.DoesNotExist:
        raise HttpError(404, f"Category with id {category_id} not found")

@api.delete("/categories/{category_id}", response=dict)
def delete_category(request, category_id: int):
    try:
        category = Category.objects.get(id=category_id)
        category.delete()
        return {"success": True}
    except Category.DoesNotExist:
        raise HttpError(404, f"Category with id {category_id} not found")

# CRUD Endpoints for Item
@api.post("/items", response=ItemSchema)
def create_item(request, payload: ItemSchema):
    item = Item.objects.create(**payload.dict())
    return item

@api.get("/items/{item_id}", response=ItemSchema)
def retrieve_item(request, item_id: int):
    try:
        return Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        raise HttpError(404, f"Item with id {item_id} not found")

@api.put("/items/{item_id}", response=ItemSchema)
def update_item(request, item_id: int, payload: ItemSchema):
    try:
        item = Item.objects.get(id=item_id)
        for attr, value in payload.dict().items():
            setattr(item, attr, value)
        item.save()
        return item
    except Item.DoesNotExist:
        raise HttpError(404, f"Item with id {item_id} not found")

@api.delete("/items/{item_id}", response=dict)
def delete_item(request, item_id: int):
    try:
        item = Item.objects.get(id=item_id)
        item.delete()
        return {"success": True}
    except Item.DoesNotExist:
        raise HttpError(404, f"Item with id {item_id} not found")

# CRUD Endpoints for GameItem
@api.post("/game-items", response=GameItemSchema)
def create_game_item(request, payload: GameItemSchema):
    game_item = GameItem.objects.create(**payload.dict())
    return game_item

@api.get("/game-items/{game_item_id}", response=GameItemSchema)
def retrieve_game_item(request, game_item_id: int):
    try:
        return GameItem.objects.get(id=game_item_id)
    except GameItem.DoesNotExist:
        raise HttpError(404, f"GameItem with id {game_item_id} not found")

@api.put("/game-items/{game_item_id}", response=GameItemSchema)
def update_game_item(request, game_item_id: int, payload: GameItemSchema):
    try:
        game_item = GameItem.objects.get(id=game_item_id)
        for attr, value in payload.dict().items():
            setattr(game_item, attr, value)
        game_item.save()
        return game_item
    except GameItem.DoesNotExist:
        raise HttpError(404, f"GameItem with id {game_item_id} not found")

@api.delete("/game-items/{game_item_id}", response=dict)
def delete_game_item(request, game_item_id: int):
    try:
        game_item = GameItem.objects.get(id=game_item_id)
        game_item.delete()
        return {"success": True}
    except GameItem.DoesNotExist:
        raise HttpError(404, f"GameItem with id {game_item_id} not found")

# CRUD Endpoints for HighScore
@api.post("/highscores", response=HighScoreSchema)
def create_highscore(request, payload: HighScoreSchema):
    highscore = HighScore.objects.create(**payload.dict())
    return highscore

@api.get("/highscores/{highscore_id}", response=HighScoreSchema)
def retrieve_highscore(request, highscore_id: int):
    try:
        return HighScore.objects.get(id=highscore_id)
    except HighScore.DoesNotExist:
        raise HttpError(404, f"HighScore with id {highscore_id} not found")

@api.put("/highscores/{highscore_id}", response=HighScoreSchema)
def update_highscore(request, highscore_id: int, payload: HighScoreSchema):
    try:
        highscore = HighScore.objects.get(id=highscore_id)
        for attr, value in payload.dict().items():
            setattr(highscore, attr, value)
        highscore.save()
        return highscore
    except HighScore.DoesNotExist:
        raise HttpError(404, f"HighScore with id {highscore_id} not found")

@api.delete("/highscores/{highscore_id}", response=dict)
def delete_highscore(request, highscore_id: int):
    try:
        highscore = HighScore.objects.get(id=highscore_id)
        highscore.delete()
        return {"success": True}
    except HighScore.DoesNotExist:
        raise HttpError(404, f"HighScore with id {highscore_id} not found")