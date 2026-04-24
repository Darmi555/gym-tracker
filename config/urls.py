from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("workouts.urls", namespace="workouts")),
    path('accounts/', include('accounts.urls')),
]
