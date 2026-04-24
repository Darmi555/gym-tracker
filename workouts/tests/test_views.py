from django.contrib.auth import get_user, get_user_model
from django.test import TestCase
from django.urls import reverse

from workouts.forms import WorkoutItemForm
from workouts.models import Workout, Exercise, GymUser, WorkoutItem, Category


class IndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.testuser = get_user_model().objects.create_user(
            username="testuser",
            password="testuser123"
        )
        cls.workout = Workout.objects.create(
            title="testworkout",
            user=cls.testuser,
        )
        cls.workout1 = Workout.objects.create(
            title="testworkout1",
            user=cls.testuser,
        )
        cls.workout2 = Workout.objects.create(
            title="testworkout2",
            user=cls.testuser,
        )
        cls.exercise = Exercise.objects.create(
            name="testexercise",
        )
        cls.exercise1 = Exercise.objects.create(
            name="testexercise1",
        )
        cls.INDEX = reverse("workouts:index")

    def test_user_login_required_logged_in(self):
        self.client.force_login(self.testuser)
        response = self.client.get(self.INDEX)
        self.assertEqual(response.status_code, 200)

    def test_user_login_required_not_logged_in(self):
        response = self.client.get(self.INDEX)
        self.assertRedirects(response, reverse("login") + "?next=" + self.INDEX)

    def test_index_context_value(self):
        self.client.force_login(self.testuser)
        response = self.client.get(self.INDEX)
        self.assertEqual(response.context["num_gym_users"], 1)
        self.assertEqual(response.context["num_workouts"], 3)
        self.assertEqual(response.context["num_exercises"], 2)

    def test_index_context_visit_count(self):
        self.client.force_login(self.testuser)
        response1 = self.client.get(self.INDEX)
        self.assertEqual(response1.context["num_visits"], 1)
        response2 = self.client.get(self.INDEX)
        self.assertEqual(response2.context["num_visits"], 2)


class WorkoutListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = get_user_model().objects.create_user(
            username="testuser1",
            password="testuser1"
        )
        cls.user2 = get_user_model().objects.create_user(
            username="testuser2",
            password="testuser2"
        )
        for i in range(16):
            Workout.objects.create(
                user=cls.user1,
                title=f"testworkout{i}{cls.user1}",
            )
        for i in range(2):
            Workout.objects.create(
                user=cls.user2,
                title=f"testworkout{i}{cls.user2}"
            )
        cls.workout_list = reverse("workouts:workout-list")

    def test_workout_list_view_logged_in(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.workout_list)
        self.assertEqual(response.status_code, 200)

    def test_workout_list_view_not_logged_in(self):
        response = self.client.get(self.workout_list)
        self.assertRedirects(response, reverse("login") + "?next=" + self.workout_list)

    def test_workout_list_view_pagination(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.workout_list)
        count = len(response.context["workout_list"])
        self.assertEqual(count, 15)
        self.assertTrue(response.context["is_paginated"])

    def test_workout_list_view_isolation(self):
        self.client.force_login(self.user2)
        response = self.client.get(self.workout_list)
        count = len(response.context["workout_list"])
        self.assertEqual(count, 2)
        titles = [workout.title for workout in response.context["workout_list"]]
        self.assertIn("testworkout0testuser2", titles)
        self.assertIn("testworkout1testuser2", titles)

    def test_workout_list_view_search_query(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.workout_list, {"q": "testworkout5testuser1"})
        count = len(response.context["workout_list"])
        self.assertEqual(count, 1)
        titles = [workout.title for workout in response.context["workout_list"]]
        self.assertIn("testworkout5testuser1", titles)


class WorkoutDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = get_user_model().objects.create_user(
            username="testuser1",
            password="testuser1"
        )
        cls.user2 = get_user_model().objects.create_user(
            username="testuser2",
            password="testuser2"
        )
        cls.workout = Workout.objects.create(
            user=cls.user1,
            title="testworkout",
        )
        cls.exercise = Exercise.objects.create(name="testexercise")
        cls.set_count = 3
        cls.rep_count = 3
        cls.weight = 3
        cls.workout_item = WorkoutItem.objects.create(
            workout=cls.workout,
            exercise=cls.exercise,
            set_count=cls.set_count,
            rep_count=cls.rep_count,
            weight=cls.weight,
        )
        cls.detail_url = reverse("workouts:workout-detail", kwargs={"pk": cls.workout.pk})

    def test_workout_detail_view_logged_in(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)

    def test_workout_detail_view_not_logged_in(self):
        response = self.client.get(self.detail_url)
        self.assertRedirects(response, reverse("login") + "?next=" + self.detail_url)

    def test_workout_detail_view_wokoutitemform(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.detail_url)
        self.assertTrue(isinstance(response.context["form"], WorkoutItemForm))

    def test_workout_detail_view_isolation(self):
        self.client.force_login(self.user2)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 404)


class WorkoutCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            password="testuser"
        )
        cls.create_url = reverse("workouts:workout-create")

    def test_workout_create_view_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code,200)

    def test_workout_create_view_not_logged_in(self):
        response = self.client.get(self.create_url)
        self.assertRedirects(response, reverse("login") + "?next=" + self.create_url)

    def test_workout_create_view_creation_successful(self):
        self.client.force_login(self.user)
        count = Workout.objects.count()
        response = self.client.post(self.create_url, data={"title": "testworkout", "date": "2026-04-23 21:00:00"})
        self.assertEqual(Workout.objects.count(), count + 1)
        self.assertEqual(response.status_code, 302)

    def test_workout_create_view_creation_unsuccessful(self):
        self.client.force_login(self.user)
        response = self.client.post(self.create_url, data={})
        self.assertEqual(response.status_code, 200)


class WorkoutUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = get_user_model().objects.create_user(
            username="testuser1",
            password="testuser1"
        )
        cls.user2 = get_user_model().objects.create_user(
            username="testuser2",
            password="testuser2"
        )
        cls.workout = Workout.objects.create(
            user=cls.user1,
            title="testworkout",
        )
        cls.update_url = reverse("workouts:workout-update", kwargs={"pk": cls.workout.pk})

    def test_workout_update_view_logged_in(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code,200)

    def test_workout_update_view_not_logged_in(self):
        response = self.client.get(self.update_url)
        self.assertRedirects(response, reverse("login") + "?next=" + self.update_url)

    def test_workout_update_view_update_successful(self):
        self.client.force_login(self.user1)
        response = self.client.post(self.update_url, data={"title": "testworkoutupdate", "date": "2026-04-23 21:00:00"})
        title = Workout.objects.get(pk=self.workout.pk).title
        self.assertEqual(title, "testworkoutupdate")
        self.assertEqual(response.status_code, 302)

    def test_workout_update_view_isolation(self):
        self.client.force_login(self.user2)
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 404)


class WorkoutDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = get_user_model().objects.create_user(
            username="testuser1",
            password="testuser1"
        )
        cls.user2 = get_user_model().objects.create_user(
            username="testuser2",
            password="testuser2"
        )
        cls.workout = Workout.objects.create(
            user=cls.user1,
            title="testworkout",
        )
        cls.delete_url = reverse("workouts:workout-delete", kwargs={"pk": cls.workout.pk})

    def test_workout_delete_view_logged_in(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code,200)

    def test_workout_delete_view_not_logged_in(self):
        response = self.client.get(self.delete_url)
        self.assertRedirects(response, reverse("login") + "?next=" + self.delete_url)

    def test_workout_delete_view_successful(self):
        self.client.force_login(self.user1)
        count_before = Workout.objects.count()
        response = self.client.post(self.delete_url, data={})
        count_after = Workout.objects.count()
        self.assertEqual(count_before, count_after + 1)
        self.assertEqual(response.status_code, 302)

    def test_workout_delete_view_isolation(self):
        self.client.force_login(self.user2)
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 404)


class WorkoutItemCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = get_user_model().objects.create_user(
            username="testuser1",
            password="testuser1"
        )
        cls.user2 = get_user_model().objects.create_user(
            username="testuser2",
            password="testuser2"
        )
        cls.workout = Workout.objects.create(
            user=cls.user1,
            title="testworkout",
        )
        cls.exercise = Exercise.objects.create(
            name="testexercise",
        )
        cls.set_count = 5
        cls.rep_count = 5
        cls.weight = 5
        cls.create_url = reverse("workouts:workout-item-create", kwargs={"workout_pk": cls.workout.pk})

    def test_workout_item_create_view_logged_in(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)

    def test_workout_item_create_view_not_logged_in(self):
        response = self.client.get(self.create_url)
        self.assertRedirects(response, reverse("login") + "?next=" + self.create_url)

    def test_workout_item_create_view_isolation(self):
        self.client.force_login(self.user2)
        response = self.client.post(
            self.create_url,
            data={
                "workout": self.workout.pk,
                "exercise": self.exercise.pk,
                "set_count": self.set_count,
                "rep_count": self.rep_count,
                "weight": self.weight
            }
        )
        self.assertEqual(response.status_code, 404)

    def test_workout_item_create_view_success(self):
        self.client.force_login(self.user1)
        count_before = WorkoutItem.objects.count()
        response = self.client.post(
            self.create_url,
            data={
                "workout": self.workout.pk,
                "exercise": self.exercise.pk,
                "set_count": self.set_count,
                "rep_count": self.rep_count,
                "weight": self.weight
            }
        )
        count_after = WorkoutItem.objects.count()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(count_after, count_before + 1)


class WorkoutItemUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = get_user_model().objects.create_user(
            username="testuser1",
            password="testuser1"
        )
        cls.user2 = get_user_model().objects.create_user(
            username="testuser2",
            password="testuser2"
        )
        cls.workout = Workout.objects.create(
            user=cls.user1,
            title="testworkout",
        )
        cls.exercise = Exercise.objects.create(
            name="testexercise",
        )
        cls.set_count = 5
        cls.rep_count = 5
        cls.weight = 5
        cls.workout_item = WorkoutItem.objects.create(
            workout=cls.workout,
            exercise=cls.exercise,
            set_count=cls.set_count,
            rep_count=cls.rep_count,
            weight=cls.weight
        )
        cls.update_url = reverse("workouts:workout-item-update", kwargs={"pk": cls.workout_item.pk})

    def test_workout_item_update_view_logged_in(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)

    def test_workout_item_update_view_not_logged_in(self):
        response = self.client.get(self.update_url)
        self.assertRedirects(response, reverse("login") + "?next=" + self.update_url)

    def test_workout_item_update_view_isolation(self):
        self.client.force_login(self.user2)
        response = self.client.post(
            self.update_url,
            data={
                "workout":self.workout.pk,
                "exercise":self.exercise.pk,
                "set_count": 3,
                "rep_count": 3,
                "weight": 3,
            }
        )
        self.assertEqual(response.status_code, 404)

    def test_workout_item_update_view_success(self):
        self.client.force_login(self.user1)
        response = self.client.post(
            self.update_url,
            data={
                "workout":self.workout.pk,
                "exercise":self.exercise.pk,
                "set_count": 5,
                "rep_count": 5,
                "weight": 3,
            }
        )
        self.assertEqual(response.status_code, 302)
        workout_item = WorkoutItem.objects.get(pk=self.workout_item.pk)
        self.assertEqual(workout_item.weight, 3)


class WorkoutItemDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = get_user_model().objects.create_user(
            username="testuser1",
            password="testuser1"
        )
        cls.user2 = get_user_model().objects.create_user(
            username="testuser2",
            password="testuser2"
        )
        cls.workout = Workout.objects.create(
            user=cls.user1,
            title="testworkout",
        )
        cls.exercise = Exercise.objects.create(
            name="testexercise",
        )
        cls.set_count = 5
        cls.rep_count = 5
        cls.weight = 5
        cls.workout_item = WorkoutItem.objects.create(
            workout=cls.workout,
            exercise=cls.exercise,
            set_count=cls.set_count,
            rep_count=cls.rep_count,
            weight=cls.weight
        )
        cls.delete_url = reverse("workouts:workout-item-delete", kwargs={"pk": cls.workout_item.pk})

    def test_workout_item_delete_view_logged_in(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)

    def test_workout_item_delete_view_not_logged_in(self):
        response = self.client.get(self.delete_url)
        self.assertRedirects(response, reverse("login") + "?next=" + self.delete_url)

    def test_workout_item_delete_view_isolation(self):
        self.client.force_login(self.user2)
        response = self.client.post(self.delete_url, data={})
        self.assertEqual(response.status_code, 404)

    def test_workout_item_delete_view_success(self):
        self.client.force_login(self.user1)
        count_before = WorkoutItem.objects.count()
        response = self.client.post(self.delete_url, data={})
        count_after = WorkoutItem.objects.count()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(count_before, count_after + 1)


class ExerciseListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            password="testuser",
        )
        cls.category1 = Category.objects.create(
            name="testcategory1",
        )
        cls.category2 = Category.objects.create(
            name="testcategory2",
        )
        cls.exercise1 = Exercise.objects.create(
            name="testexercise1",
            description="description test",
        )
        cls.exercise1.categories.add(cls.category1)
        cls.exercise2 = Exercise.objects.create(
            name="testexercise2",
        )
        cls.exercise2.categories.add(cls.category2)
        cls.exercise_url = reverse("workouts:exercise-list")

    def test_exercise_list_view_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(self.exercise_url)
        self.assertEqual(response.status_code, 200)

    def test_exercise_list_view_not_logged_in(self):
        response = self.client.get(self.exercise_url)
        self.assertRedirects(response, reverse("login") + "?next=" + self.exercise_url)

    def test_exercise_list_view_search_name(self):
        self.client.force_login(self.user)
        response = self.client.get(self.exercise_url, {"q": "testexercise1"})
        exercise_list = response.context["exercise_list"]
        self.assertEqual(len(exercise_list), 1)
        self.assertEqual(exercise_list[0].name, "testexercise1")

    def test_exercise_list_view_search_description(self):
        self.client.force_login(self.user)
        response = self.client.get(self.exercise_url, {"q": "description"})
        exercise_list = response.context["exercise_list"]
        self.assertEqual(len(exercise_list), 1)
        self.assertEqual(exercise_list[0].name, "testexercise1")

    def test_exercise_list_view_search_category(self):
        self.client.force_login(self.user)
        response = self.client.get(self.exercise_url, {"category": self.category1.id})
        exercise_list = response.context["exercise_list"]
        self.assertEqual(len(exercise_list), 1)
        self.assertEqual(exercise_list[0].name, "testexercise1")


class ExerciseDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = get_user_model().objects.create_user(
            username="testuser1",
            password="testuser1",
        )
        cls.user2 = get_user_model().objects.create_user(
            username="testuser2",
            password="testuser2",
        )
        cls.exercise = Exercise.objects.create(
            name="testexercise",
        )
        cls.workout1 = Workout.objects.create(
            user=cls.user1,
            title="testworkout1",
        )
        cls.workoutitem1 = WorkoutItem.objects.create(
            workout=cls.workout1,
            exercise=cls.exercise,
            set_count=5,
            rep_count=5,
            weight=5,
        )
        cls.workout2 = Workout.objects.create(
            user=cls.user2,
            title="testworkout2",
        )
        cls.workoutitem2 = WorkoutItem.objects.create(
            workout=cls.workout2,
            exercise=cls.exercise,
            set_count=7,
            rep_count=7,
            weight=7,
        )
        cls.detail_url = reverse("workouts:exercise-detail", kwargs={"pk": cls.exercise.pk})

    def test_exercise_detail_view_logged_in(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)

    def test_exercise_detail_view_not_logged_in(self):
        response = self.client.get(self.detail_url)
        self.assertRedirects(response, reverse("login") + "?next=" + self.detail_url)

    def test_exercise_detail_view_history(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.detail_url)
        workout_item_list = response.context["history"]
        self.assertEqual(len(workout_item_list), 1)
        self.assertEqual(workout_item_list[0].set_count, 5)


class CategoryListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            password="testuser",
        )
        cls.category_url = reverse("workouts:category-list")

    def test_category_list_view_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(self.category_url)
        self.assertEqual(response.status_code, 200)

    def test_category_list_view_not_logged_in(self):
        response = self.client.get(self.category_url)
        self.assertRedirects(response, reverse("login") + "?next=" + self.category_url)
