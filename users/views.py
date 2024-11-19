"""Accounts view."""

from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView

from users.forms import CustomUserCreationForm
from users.models import CustomUser, Password

from .mixins import CustomLoginRequiredMixin, PaidUserRequiredMixin


class SignUpView(CreateView):
    """User registration view."""

    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")
    extra_context = {"title_text": "Sign Up", "button_text": "Register"}


class UserListView(UserPassesTestMixin, generic.ListView):
    """List of each users."""

    model = CustomUser
    queryset = CustomUser.objects.order_by("-date_joined")
    template_name = "user_list.html"

    def test_func(self):
        # Only allow access if the user is a superuser
        if not self.request.user.is_superuser:
            raise PermissionDenied  # noqa: F821
        return True


class UserDetailView(UserPassesTestMixin, generic.DetailView):
    """Detail view for a user."""

    model = CustomUser
    template_name = "user_detail.html"  # The template you want to use
    context_object_name = "user"  # Name to reference in the template

    def test_func(self):
        # Only allow access if the user is a superuser
        if not self.request.user.is_superuser:
            raise PermissionDenied  # noqa: F821
        return True


class UpdateUserView(UserPassesTestMixin, generic.UpdateView):
    """View to update user details."""

    model = CustomUser
    fields = ["first_name", "last_name", "email"]  # Add any fields you want to allow editing
    template_name = "generic_create_update_form.html"
    success_url = reverse_lazy("users:user-list")  # Redirect after update
    extra_context = {"title_text": "Update User", "button_text": "Update"}

    def test_func(self):
        # Only allow access if the user is a superuser
        if not self.request.user.is_superuser:
            raise PermissionDenied  # noqa: F821
        return True


class DeleteUserView(UserPassesTestMixin, generic.DeleteView):
    """View to delete a user."""

    model = CustomUser
    template_name = "generic_confirm_delete.html"  # This template will ask for confirmation
    success_url = reverse_lazy("users:user-list")  # Redirect to the user list after deletion

    def test_func(self):
        # Only allow access if the user is a superuser
        if not self.request.user.is_superuser:
            raise PermissionDenied  # noqa: F821
        return True


class CreatePasswordView(PaidUserRequiredMixin, generic.CreateView):
    """View to create passwords"""

    model = Password
    fields = ["website", "website_username", "password_encrypted"]
    success_url = reverse_lazy("users:password-list")
    template_name = "generic_create_update_form.html"
    extra_context = {"title_text": "Add Stored Password", "button_text": "Add"}

    # Optionally, specify the login URL and a redirect field name
    login_url = "/accounts/login/"  # Change to your login path

    def form_valid(self, form):  # noqa: D102
        # Set the user to the currently logged-in user
        form.instance.user = self.request.user
        return super().form_valid(form)


class PasswordListView(PaidUserRequiredMixin, generic.ListView):
    """View to list passwords created by the logged-in user"""

    model = Password
    template_name = "password_list.html"  # Replace with your actual template path
    context_object_name = "passwords"

    def get_queryset(self):  # noqa: D102
        # Filter passwords by the logged-in user
        return Password.objects.filter(user=self.request.user)


class PasswordDetailView(PaidUserRequiredMixin, generic.DetailView):
    """Detail"""

    model = Password
    template_name = "password_details.html"


class PasswordUpdateView(PaidUserRequiredMixin, generic.UpdateView):
    """Updating passwords"""

    model = Password
    fields = ["website", "website_username", "password_encrypted"]
    success_url = reverse_lazy("users:password-list")
    template_name = "generic_create_update_form.html"
    extra_context = {"title_text": "Update Stored Password", "button_text": "Update"}


class DeletePasswordView(PaidUserRequiredMixin, generic.DeleteView):
    """Deleting passwords"""

    model = Password
    success_url = reverse_lazy("users:password-list")
    template_name = "generic_confirm_delete.html"
    extra_context = {"title_text": "Delete Stored Password"}


class StrengthCheckerView(CustomLoginRequiredMixin, generic.TemplateView):
    """View to display the password strength checker page."""

    success_url = reverse_lazy("users:strength-checker")
    template_name = "strength_checker.html"
    login_url = "/accounts/login/"  # Ensure this path matches your project's login path
