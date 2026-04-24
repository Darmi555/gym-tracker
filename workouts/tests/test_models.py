from django.contrib.auth import get_user_model
from django.test import TestCase

from workouts.models import Category, Exercise, Workout, WorkoutItem


class GymUserModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
        )

    def test_gym_user_str(self):
        self.assertEqual(str(self.user), "testuser")


    def test_gym_user_optional_fields(self):
        self.user.full_clean()
        self.assertIsNone(self.user.years_of_experience)
        self.assertIsNone(self.user.description)


class CategoryModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="testcategory")

    def test_category_str(self):
        self.assertEqual(str(self.category), "testcategory")


class ExerciseModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.exercise = Exercise.objects.create(name="testexercise")

    def test_exercise_str(self):
        self.assertEqual(str(self.exercise), "testexercise")

    def test_exercise_optional_fields(self):
        self.exercise.full_clean()
        self.assertIsNone(self.exercise.description)

    def test_exercise_related_name(self):
        category = Category.objects.create(name="testcategory")
        self.exercise.categories.add(category)
        self.assertIn(self.exercise, category.exercises.all())


class WorkoutModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
        )
        cls.workout = Workout.objects.create(
            title="testworkout",
            user=cls.user,
        )

    def test_workout_str(self):
        self.assertEqual(str(self.workout), "testworkout")

    def test_workout_optional_fields(self):
        self.workout.full_clean()
        self.assertIsNone(self.workout.description)

    def test_workout_user_cascade(self):
        self.user.delete()
        count = Workout.objects.count()
        self.assertEqual(count, 0)


class WorkoutItemModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
        )
        cls.workout = Workout.objects.create(
            title="testworkout",
            user=cls.user,
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

    def test_workout_item_str(self):
        self.assertEqual(str(self.workout_item),"testexercise (3x3) - testworkout")

    def test_workout_item_workout_cascade(self):
        self.workout.delete()
        count = WorkoutItem.objects.count()
        self.assertEqual(count, 0)

    def test_workout_item_exercise_cascade(self):
        self.exercise.delete()
        count = WorkoutItem.objects.count()
        self.assertEqual(count, 0)

    def test_workout_item_related_name(self):
        count = self.workout.items.count()
        self.assertEqual(count, 1)
