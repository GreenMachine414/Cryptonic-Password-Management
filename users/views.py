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


class CreateUserView(generic.CreateView):
    """View to create user"""

    model = CustomUser
    fields = ["first_name"]
    success_url = reverse_lazy("users:user-list")
    template_name = "generic_create_update_form.html"
    extra_context = {"title_text": "Add User", "button_text": "Add"}


class UserListView(generic.ListView):
    """List of each users"""

    model = CustomUser
    queryset = CustomUser.objects.order_by("-date_joined")
    template_name = "users/templates/generic_create_update_form.html"
