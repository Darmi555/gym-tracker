from django import forms
from .models import Workout, WorkoutItem


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ["title", "date", "description"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Monday - Full Body Workout",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Optional notes, how are you feeling today?",
                }
            ),
            "date": forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                }
            ),
        }


class WorkoutItemForm(forms.ModelForm):
    class Meta:
        model = WorkoutItem
        fields = ["exercise", "set_count", "rep_count", "weight"]
        widgets = {
            "exercise": forms.Select(attrs={"class": "form-control"}),
            "set_count": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
            "rep_count": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
            "weight": forms.NumberInput(
                attrs={"class": "form-control", "min": "0.25", "step": "0.25"}
            ),
        }
