from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

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


class WorkoutListView(LoginRequiredMixin, generic.ListView):
    model = Workout
    paginate_by = 10

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user)


class WorkoutDetailView(LoginRequiredMixin, generic.DetailView):
    model = Workout

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user)


class ExerciseListView(LoginRequiredMixin, generic.ListView):
    model = Exercise
    paginate_by = 10


class ExerciseDetailView(LoginRequiredMixin, generic.DetailView):
    model = Exercise


class CategoryListView(LoginRequiredMixin, generic.ListView):
    model = Category
    paginate_by = 10


class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    model = Category
