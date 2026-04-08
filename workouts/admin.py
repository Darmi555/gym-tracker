from django.contrib import admin

from workouts.models import Category, Exercise


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "get_category", "description",)

    def get_category(self, obj):
        return ", ".join([cat.name for cat in obj.categories.all()])
    get_category.short_description = "Category"