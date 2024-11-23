"""Accounts view."""

import random
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic
from django.views.generic import CreateView

from users.forms import CustomUserCreationForm
from users.models import CustomUser, Password

from .mixins import CustomLoginRequiredMixin, PaidUserRequiredMixin
from .models import OTPCode


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
    template_name = "password_list.html"
    context_object_name = "passwords"

    def get_queryset(self):
        passwords = Password.objects.filter(user=self.request.user)
        for password in passwords:
            password.decrypted = password.decrypt_password()
        return passwords


class PasswordDetailView(PaidUserRequiredMixin, generic.DetailView):
    """Detail view for individual passwords"""

    model = Password
    template_name = "password_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["decrypted_password"] = self.object.decrypt_password()
        return context


class PasswordUpdateView(PaidUserRequiredMixin, generic.UpdateView):
    """Updating passwords"""

    model = Password
    fields = ["website", "website_username", "password_encrypted"]
    template_name = "password_update.html"
    extra_context = {"title_text": "Update Stored Password", "button_text": "Update"}

    def get_success_url(self):
        return reverse_lazy("users:password-detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        # Get the original encrypted password before update
        original_password = Password.objects.get(pk=self.object.pk)

        # Only encrypt if password was changed
        if form.cleaned_data["password_encrypted"] != original_password.decrypt_password():
            form.instance.password_encrypted = form.instance.encrypt_password(
                form.cleaned_data["password_encrypted"]
            )
        else:
            form.instance.password_encrypted = original_password.password_encrypted

        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        # Show decrypted password in form
        initial["password_encrypted"] = self.object.decrypt_password()
        return initial


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


class PasswordGeneratorView(CustomLoginRequiredMixin, generic.TemplateView):
    """View to display the password strength checker page."""

    success_url = reverse_lazy("users:password-generator")
    template_name = "password_generator.html"
    login_url = "/accounts/login/"  # Ensure this path matches your project's login path


class SubscriptionView(CustomLoginRequiredMixin, generic.TemplateView):  # noqa: D101
    template_name = "subscription.html"

    def post(self, request, *args, **kwargs):
        # Process payment here
        user = request.user
        user.is_paid = True
        user.save()
        return redirect("users:password-list")


class PlanView(PaidUserRequiredMixin, generic.TemplateView):  # noqa: D101
    template_name = "plan.html"

    def post(self, request, *args, **kwargs):
        # Process payment here
        user = request.user
        user.is_paid = True
        user.save()
        return redirect("users:password-list")


class EndSubscriptionView(PaidUserRequiredMixin, generic.TemplateView):
    def post(self, request):
        user = request.user
        user.is_paid = False
        user.save()
        messages.success(request, "Your subscription has been cancelled.")
        return redirect("users:password-list")


class LoginMFAView(generic.TemplateView):
    def post(self, request):
        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        if user:
            code = "".join([str(random.randint(0, 9)) for _ in range(6)])
            expires_at = timezone.now() + timedelta(minutes=10)

            OTPCode.objects.create(user=user, code=code, expires_at=expires_at)

            send_mail(
                "Your Login Code",
                f"Your verification code is: {code}",
                "Taylormichaelandrus@gmail.com",  # Update this to match EMAIL_HOST_USER
                [user.email],
                fail_silently=False,
            )

            request.session["mfa_user_id"] = user.id
            return redirect("users:verify-mfa")


class VerifyMFAView(generic.TemplateView):
    template_name = "verify_mfa.html"

    def post(self, request):
        code = request.POST["code"]
        user_id = request.session.get("mfa_user_id")

        otp = OTPCode.objects.filter(
            user_id=user_id, code=code, expires_at__gt=timezone.now()
        ).first()

        if otp:
            login(request, otp.user)
            otp.delete()
            return redirect("home")

        # Handle invalid code case
        return render(request, self.template_name, {"error": "Invalid verification code"})
