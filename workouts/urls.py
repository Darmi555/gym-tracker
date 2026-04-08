from django.urls import path

from workouts.views import index


urlpatterns = [
    path("", index, name="index"),
]

app_name = "workouts"
