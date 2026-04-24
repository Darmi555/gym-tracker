from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class RegistrationViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.register_url = reverse("register")

    def test_register_view_status_code(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)

    def test_register_view_success(self):
        count_before = get_user_model().objects.count()
        response = self.client.post(
            self.register_url,
            data={
                "username": "testusername",
                "email": "test@email.com",
                "password1": "testpassword",
                "password2": "testpassword",
            }
        )
        count_after = get_user_model().objects.count()
        self.assertEqual(count_after, count_before + 1)
        self.assertRedirects(response, reverse("login"))

    def test_register_view_failed(self):
        count_before = get_user_model().objects.count()
        response = self.client.post(
            self.register_url,
            data={}
        )
        count_after = get_user_model().objects.count()
        self.assertEqual(count_after, count_before)
        self.assertEqual(response.status_code, 200)


class AuthViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            password="testuser123",
        )

    def test_login_view_status_code(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_logout_view_redirects(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, 302)
