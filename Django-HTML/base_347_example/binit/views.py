from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from .models import Game, GameItem, Item, Category, HighScore
from django.urls import reverse
from django.http import JsonResponse
import random, json

# Create your views here.
def index(request):
    high_score = None
    if request.user.is_authenticated and not isinstance(request.user, AnonymousUser):
        high_score = HighScore.objects.filter(user=request.user).order_by('-score').first()
    return render(request, "binit/index.html", {'high_score': high_score})

@login_required
def start_game(request):
    # Create a new game for the logged-in user
    game = Game.objects.create(user=request.user)

    # Select a random set of items (e.g., 10 items)
    items = list(Item.objects.all())
    random.shuffle(items)
    selected_items = items[:10]

    # Create GameItem entries
    for item in selected_items:
        GameItem.objects.create(game=game, item=item)

    # Save game ID to session
    request.session['current_game_id'] = game.id

    return redirect('binit:play_game')

@login_required
def play_game(request):
    # Use sessions to track the current game
    game_id = request.session.get('current_game_id')
    if not game_id:
        return redirect('binit:start_game')  # fallback if session is empty
    
    game = get_object_or_404(Game, id=game_id, user=request.user)

    if request.method == 'POST':
        try:
            # Get the guesses_json field from the form data
            guesses_json = request.POST.get('guesses_json', '{}')
            guesses = json.loads(guesses_json)  # Parse the JSON string

            correct_count = 0
            incorrect_count = 0

            for item_id, guessed_category_id in guesses.items():
                game_item = GameItem.objects.get(game=game, item_id=item_id)
                guessed_category = Category.objects.get(id=guessed_category_id)
                game_item.guessed_category = guessed_category
                game_item.is_correct = (guessed_category == game_item.item.correct_category)
                game_item.save()

                if game_item.is_correct:
                    correct_count += 1
                else:
                    incorrect_count += 1

            # Calculate time taken
            game.end_time = timezone.now()
            time_taken = (game.end_time - game.start_time).total_seconds()

            # Scoring system
            base_score = correct_count * 15  # 10 points per correct answer
            time_penalty = int(time_taken / 20)  # Deduct 1 point for every 10 seconds
            incorrect_penalty = incorrect_count * 3  # Deduct 5 points per incorrect answer
            time_bonus = 10 if time_taken < 60 else 0  # Bonus for finishing under 1 minute
            perfect_score_bonus = 50 if correct_count == game.game_items.count() else 0  # Bonus for perfect score

            # Final score
            final_score = max(base_score - time_penalty - incorrect_penalty + time_bonus + perfect_score_bonus, 0)
            game.score = final_score
            game.save()

            # Check if this is a new high score
            high_score = HighScore.objects.filter(user=request.user).order_by('-score').first()
            if not high_score or game.score > high_score.score:
                HighScore.objects.create(user=request.user, score=game.score)

            # Return a JSON response with the redirect URL
            return JsonResponse({'redirect_url': reverse('binit:game_results')})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    # GET request: render the play page
    game_items = GameItem.objects.filter(game=game)
    categories = Category.objects.all()

    return render(request, 'binit/play_game.html', {
        'game': game,
        'game_items': game_items,
        'categories': categories,
    })

@login_required
def game_result(request):
    # Use sessions to track the current game
    game_id = request.session.get('current_game_id')
    if not game_id:
        return redirect('binit:start_game')
    
    game = get_object_or_404(Game, id=game_id, user=request.user)
    game_items = GameItem.objects.filter(game=game)

    # Calculate time taken as timedelta
    time_taken = None
    if game.end_time and game.start_time:
        time_taken = game.end_time - game.start_time

    # Convert to minutes and seconds
    minutes, seconds = divmod(time_taken.total_seconds(), 60) if time_taken else (0, 0)
    time_str = f"{int(minutes)}m {int(seconds)}s"

    correct_count = game_items.filter(is_correct=True).count()
    incorrect_count = game_items.filter(is_correct=False).count()

    # Fetch the user's high score
    high_score = HighScore.objects.filter(user=request.user).order_by('-score').first()

    return render(request, 'binit/game_result.html', {
        'game': game,
        'game_items': game_items,
        'correct_count': correct_count,
        'incorrect_count': incorrect_count,
        'time_str': time_str,
        'high_score': high_score,
    })
