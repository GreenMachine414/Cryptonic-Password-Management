"""Accounts models."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.managers import CustomUserManager


class CustomUser(AbstractUser):
    """A custom User model.

    Arguments:
    ---------
    AbstractUser : class
        Django's `AbstractUser` class.

    Returns:
    -------
    object:
        `CustomUser` model.

    """

    username = models.CharField(_("username"), max_length=150, unique=True, blank=True, null=True)
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    is_paid = models.BooleanField(_("is paid"), default=False)
    num_stored_passwords = models.IntegerField(_("number of stored passwords"), default=0)
    paid_access_expires = models.DateTimeField(_("paid access expires"), null=True, blank=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()


def __str__(self) -> str:
    """Get the string representation of the object."""
    return self.username if self.username else str(self.id)  # Fallback to user ID


class Password(models.Model):
    """A model for storing encrypted passwords associated with a user."""

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="passwords")
    username = models.CharField(_("username"), max_length=255)
    website = models.CharField(_("website"), max_length=255)
    website_username = models.CharField(_("website username"), max_length=255)
    is_password = models.BooleanField(_("is password"), default=True)
    created = models.DateTimeField(_("created"), auto_now_add=True)
    last_used = models.DateTimeField(_("last used"), null=True, blank=True)
    password_encrypted = models.CharField(_("password encrypted"), max_length=255)

    def __str__(self):
        """Get the string representation of the object."""
        return f"{self.website} - {self.website_username}"

    class Meta:
        verbose_name = _("Password")
        verbose_name_plural = _("Passwords")
