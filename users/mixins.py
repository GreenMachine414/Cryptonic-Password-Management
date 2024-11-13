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
        return redirect(self.login_url)
