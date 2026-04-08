from django.urls import path

from workouts.views import index, WorkoutListView

urlpatterns = [
    path("", index, name="index"),
    path("workouts/", WorkoutListView.as_view(), name="workouts"),
]

app_name = "workouts"
