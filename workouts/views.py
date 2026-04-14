from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic

from workouts.models import Workout, Exercise, Category, WorkoutItem


@login_required
def index(request):
    num_gym_users = get_user_model().objects.count()
    num_workouts = Workout.objects.count()
    num_categories = Category.objects.count()
    num_exercises = Exercise.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_gym_users": num_gym_users,
        "num_workouts": num_workouts,
        "num_categories": num_categories,
        "num_exercises": num_exercises,
        "num_visits": num_visits + 1,
    }

    return render(request, "workouts/index.html", context=context)


class WorkoutListView(LoginRequiredMixin, generic.ListView):
    model = Workout
    paginate_by = 15

    def get_queryset(self):
        qs = Workout.objects.filter(user=self.request.user)
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        return qs.order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = context.get('page_obj')

        if page:
            context['custom_page_range'] = page.paginator.get_elided_page_range(
                page.number, on_each_side=1, on_ends=1
            )
        return context


class WorkoutDetailView(LoginRequiredMixin, generic.DetailView):
    model = Workout

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user)


class WorkoutCreateView(LoginRequiredMixin, generic.CreateView):
    model = Workout
    fields = ["title", "date", "description"]
    success_url = reverse_lazy("workouts:workout-list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



class WorkoutUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Workout
    fields = ["title", "date", "description"]
    success_url = reverse_lazy("workouts:workout-list")

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user)


class WorkoutDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Workout
    success_url = reverse_lazy("workouts:workout-list")

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user)


class WorkoutItemCreateView(LoginRequiredMixin, generic.CreateView):
    model = WorkoutItem
    fields = ["exercise", "set_count", "rep_count", "weight"]

    def get_success_url(self):
        workout_id = self.object.workout_id
        return reverse("workouts:workout-detail", kwargs={"pk": workout_id})

    def form_valid(self, form):
        workout = Workout.objects.get(pk=self.kwargs["workout_pk"])
        form.instance.workout = workout
        return super().form_valid(form)


class WorkoutItemUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = WorkoutItem
    fields = ["exercise", "set_count", "rep_count", "weight"]

    def get_success_url(self):
        workout_id = self.object.workout_id
        return reverse("workouts:workout-detail", kwargs={"pk": workout_id})

    def get_queryset(self):
        return WorkoutItem.objects.filter(workout__user=self.request.user)


class WorkoutItemDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = WorkoutItem

    def get_success_url(self):
        workout_id = self.object.workout_id
        return reverse("workouts:workout-detail", kwargs={"pk": workout_id})

    def get_queryset(self):
        return WorkoutItem.objects.filter(workout__user=self.request.user)


class ExerciseListView(LoginRequiredMixin, generic.ListView):
    model = Exercise
    paginate_by = 10


class ExerciseDetailView(LoginRequiredMixin, generic.DetailView):
    model = Exercise



class CategoryListView(LoginRequiredMixin, generic.ListView):
    model = Category
    paginate_by = 10


class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    model = Category


