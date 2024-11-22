from django.contrib.auth.mixins import AccessMixin
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
        # Check if there is a 'next' parameter in the request's GET data
        next_url = self.request.GET.get("next", "")
        # If there is a next parameter, append it to the login URL
        if next_url:
            return redirect(f"{self.login_url}?next={next_url}")
        # Otherwise, just redirect to the login URL
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
            return redirect("users:subscription")

        return super().dispatch(request, *args, **kwargs)
