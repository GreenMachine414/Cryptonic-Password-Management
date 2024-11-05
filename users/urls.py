"""Accounts app URL Configuration."""

from django.urls import path

from users import views as users_views

app_name = "users"

urlpatterns = [
    path("signup/", users_views.SignUpView.as_view(), name="signup"),
    path("users/add", users_views.CreateUserView.as_view(), name="create-question"),
    path("", users_views.UserListView.as_view(), name="user-list"),
]
