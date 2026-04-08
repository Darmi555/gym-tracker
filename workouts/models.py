from django.contrib.auth.models import AbstractUser
from django.db import models


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
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name

