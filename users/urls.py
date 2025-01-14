"""Accounts app URL Configuration."""

from django.urls import path

from users import views as users_views

app_name = "users"

urlpatterns = [
    path("signup/", users_views.SignUpView.as_view(), name="signup"),
    path("users/", users_views.UserListView.as_view(), name="user-list"),
    path("<int:pk>/", users_views.UserDetailView.as_view(), name="user-detail"),
    path("update/<int:pk>/", users_views.UpdateUserView.as_view(), name="update-user"),
    path("delete/<int:pk>/", users_views.DeleteUserView.as_view(), name="delete-user"),
    path("password/add", users_views.CreatePasswordView.as_view(), name="create-password"),
    path("password", users_views.PasswordListView.as_view(), name="password-list"),
    path("password/<int:pk>/", users_views.PasswordDetailView.as_view(), name="password-detail"),
    path(
        "password/<int:pk>/edit/", users_views.PasswordUpdateView.as_view(), name="update-password"
    ),
    path(
        "password/<int:pk>/delete/",
        users_views.DeletePasswordView.as_view(),
        name="delete-password",
    ),
    path(
        "password-strength-checker/",
        users_views.StrengthCheckerView.as_view(),
        name="strength-checker",
    ),
    path(
        "password-generator/",
        users_views.PasswordGeneratorView.as_view(),
        name="password-generator",
    ),
    path(
        "subscription/",
        users_views.SubscriptionView.as_view(),
        name="subscription",
    ),
    path(
        "plan/",
        users_views.PlanView.as_view(),
        name="plan",
    ),
    path("end-subscription/", users_views.EndSubscriptionView.as_view(), name="end-subscription"),
    path("login/mfa/", users_views.LoginMFAView.as_view(), name="login-mfa"),
    path("verify-mfa/", users_views.VerifyMFAView.as_view(), name="verify-mfa"),
]
