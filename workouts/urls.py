from django.urls import path

from workouts.models import Category
from workouts.views import index, WorkoutListView, WorkoutDetailView, ExerciseListView, ExerciseDetailView, \
    CategoryListView, CategoryDetailView

urlpatterns = [
    path("", index, name="index"),
    path("workouts/", WorkoutListView.as_view(), name="workout-list"),
    path("workouts/<int:pk>", WorkoutDetailView.as_view(), name="workout-detail"),
    path("exercises/", ExerciseListView.as_view(), name="exercise-list"),
    path("exercise/<int:pk>/", ExerciseDetailView.as_view(), name="exercise-detail"),
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
]

app_name = "workouts"g
