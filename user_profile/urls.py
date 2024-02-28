"""User profile app URL."""

from django.urls import path

from . import views

app_name = "user_profile"

urlpatterns = [
    path("profile/", views.UserProfileDetailView.as_view(), name="profile_detail"),
    path(
        "profile/update/", views.UserProfileUpdateView.as_view(), name="profile_update"
    ),
]
