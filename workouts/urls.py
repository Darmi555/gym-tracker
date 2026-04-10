from django.urls import path

from workouts.models import Category
from workouts.views import index, WorkoutListView, WorkoutDetailView, ExerciseListView, ExerciseDetailView, \
    CategoryListView, CategoryDetailView, WorkoutCreateView, WorkoutUpdateView, WorkoutDeleteView, WorkoutItemCreateView

urlpatterns = [
    path("", index, name="index"),
    path("workouts/", WorkoutListView.as_view(), name="workout-list"),
    path("workouts/<int:pk>", WorkoutDetailView.as_view(), name="workout-detail"),
    path("workouts/create/", WorkoutCreateView.as_view(), name="workout-create"),
    path("workouts/<int:pk>/update/", WorkoutUpdateView.as_view(), name="workout-update"),
    path("workouts/<int:pk>/delete/", WorkoutDeleteView.as_view(), name="workout-delete"),
    path("exercises/", ExerciseListView.as_view(), name="exercise-list"),
    path("exercise/<int:pk>/", ExerciseDetailView.as_view(), name="exercise-detail"),
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
    path("workouts/<int:workout_pk>/items/create/", WorkoutItemCreateView.as_view(), name="workout-item-create"),
]

app_name = "workouts"
