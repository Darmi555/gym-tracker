from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class GymUser(AbstractUser):
    years_of_experience = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Gym User"
        verbose_name_plural = "Gym Users"

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Exercise(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name="exercises")

    def __str__(self):
        return self.name


class Workout(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Workout"
        verbose_name_plural = "Workouts"


class WorkoutItem(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    set_count = models.PositiveIntegerField()
    rep_count = models.PositiveIntegerField()
    weight = models.FloatField()

