from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm  # Nasz sformatowany formularz

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',  # Ścieżka do Twojego pliku
        authentication_form=UserLoginForm
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
