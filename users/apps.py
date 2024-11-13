from django.apps import AppConfig  # noqa: D100


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        pass  # Import signals module
