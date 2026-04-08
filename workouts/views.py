from django.contrib.auth import get_user_model
from django.shortcuts import render
from workouts.models import Workout, Exercise, Category


def index(request):
    num_gym_users = get_user_model().objects.count()
    num_workouts = Workout.objects.count()
    num_categories = Category.objects.count()
    num_exercises = Exercise.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_gym_users": num_gym_users,
        "num_workouts": num_workouts,
        "num_categories": num_categories,
        "num_exercises": num_exercises,
        "num_visits": num_visits + 1,
    }

    return render(request, "workouts/index.html", context=context)
