"""Accounts view."""

from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView

from users.forms import CustomUserCreationForm
from users.models import CustomUser


class SignUpView(CreateView):
    """User registration view."""

    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "generic_create_update_form.html"
    success_url = reverse_lazy("login")
    extra_context = {"title_text": "Sign Up", "button_text": "Register"}


class CreateUserView(CreateView):
    """View to create user."""

    model = CustomUser
    fields = ["username", "email"]  # Include 'email' in the fields
    success_url = reverse_lazy("users:user-list")
    template_name = "generic_create_update_form.html"
    extra_context = {"title_text": "Add User", "button_text": "Add"}


class UserListView(generic.ListView):
    """List of each users."""

    model = CustomUser
    queryset = CustomUser.objects.order_by("-date_joined")
    template_name = "user_list.html"


class UserDetailView(generic.DetailView):
    """Detail view for a user."""

    model = CustomUser
    template_name = "user_detail.html"  # The template you want to use
    context_object_name = "user"  # Name to reference in the template


class UpdateUserView(generic.UpdateView):
    """View to update user details."""

    model = CustomUser
    fields = ["first_name", "last_name", "email"]  # Add any fields you want to allow editing
    template_name = "generic_create_update_form.html"
    success_url = reverse_lazy("users:user-list")  # Redirect after update
    extra_context = {"title_text": "Update User", "button_text": "Update"}


class DeleteUserView(generic.DeleteView):
    """View to delete a user."""

    model = CustomUser
    template_name = "generic_confirm_delete.html"  # This template will ask for confirmation
    success_url = reverse_lazy("users:user-list")  # Redirect to the user list after deletion
