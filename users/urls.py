"""Accounts app URL Configuration."""

from django.urls import path

from users import views as users_views

app_name = "users"

urlpatterns = [
    path("signup/", users_views.SignUpView.as_view(), name="signup"),
    path("users/add", users_views.CreateUserView.as_view(), name="create-user"),
    path("", users_views.UserListView.as_view(), name="user-list"),
    path("<int:pk>/", users_views.UserDetailView.as_view(), name="user-detail"),
    path("update/<int:pk>/", users_views.UpdateUserView.as_view(), name="update-user"),
    path("delete/<int:pk>/", users_views.DeleteUserView.as_view(), name="delete-user"),
]
