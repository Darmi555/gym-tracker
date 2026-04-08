from django.urls import path

from workouts.views import index, WorkoutListView, WorkoutDetailView

urlpatterns = [
    path("", index, name="index"),
    path("workouts/", WorkoutListView.as_view(), name="workouts"),
    path("workouts/<int:pk>", WorkoutDetailView.as_view(), name="workouts"),
]

app_name = "workouts"
