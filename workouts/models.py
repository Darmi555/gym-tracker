from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class GymUser(AbstractUser):
    years_of_experience = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Gym User"
        verbose_name_plural = "Gym Users"

    def __str__(self):
        return self.username
