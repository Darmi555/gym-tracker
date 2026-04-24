from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from workouts.models import Category, Exercise, GymUser, WorkoutItem, Workout


@admin.register(GymUser)
class GymUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("years_of_experience", "description",)
    fieldsets = UserAdmin.fieldsets + (("Additional information", {"fields": ("years_of_experience", "description")},),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Additional information", {"fields": ("years_of_experience", "description")},),)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "get_category", "description",)

    def get_category(self, obj):
        return ", ".join([cat.name for cat in obj.categories.all()])
    get_category.short_description = "Category"


class WorkoutItemInline(admin.TabularInline):
    model = WorkoutItem
    extra = 1


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "date", "description",)
    inlines = [WorkoutItemInline]
