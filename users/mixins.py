from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


class LoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class CustomLoginRequiredMixin(LoginRequiredMixin):  # noqa: D101
    login_url = "/accounts/login/"  # Ensure this is set to your login URL

    def handle_no_permission(self):  # noqa: D102
        return redirect(self.login_url)


class PaidUserRequiredMixin(CustomLoginRequiredMixin):
    """Mixin that ensures the user is logged in and is paid (is_paid = True)."""

    def dispatch(self, request, *args, **kwargs):
        # First, check if the user is logged in using the CustomLoginRequiredMixin behavior
        if not request.user.is_authenticated:
            return super().dispatch(
                request, *args, **kwargs
            )  # Calls the parent `dispatch` (which redirects to login)

        # Check if the user is paid
        if not request.user.is_paid:
            raise PermissionDenied("You must be a paid user to access this page.")

        return super().dispatch(request, *args, **kwargs)
