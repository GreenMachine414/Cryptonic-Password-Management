"""Accounts models."""

import base64
import secrets

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.managers import CustomUserManager


class CustomUser(AbstractUser):
    username = models.CharField(_("username"), max_length=150, unique=True, blank=True, null=True)
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    is_paid = models.BooleanField(_("is paid"), default=True)
    num_stored_passwords = models.IntegerField(_("number of stored passwords"), default=0)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()


def __str__(self) -> str:  # noqa: N807
    """Get the string representation of the object."""
    return self.username if self.username else str(self.id)


class Password(models.Model):
    """A model for storing encrypted passwords associated with a user."""

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="passwords")
    username = models.CharField(_("username"), max_length=255)
    website = models.CharField(_("website"), max_length=255)
    website_username = models.CharField(_("website username"), max_length=255)
    is_password = models.BooleanField(_("is password"), default=True)
    created = models.DateTimeField(_("created"), auto_now_add=True)
    last_used = models.DateTimeField(_("last used"), null=True, blank=True)
    password_encrypted = models.CharField(_("password"), max_length=255)

    def __str__(self):
        """Get the string representation of the object."""
        return f"{self.website} - {self.website_username}"

    def encrypt_password(self, raw_password):
        """Encrypt the password using secrets."""
        key = secrets.token_bytes(32)
        encrypted = base64.b64encode(key + raw_password.encode())
        return encrypted.decode()

    def decrypt_password(self):
        """Decrypt the stored password."""
        decoded = base64.b64decode(self.password_encrypted.encode())
        return decoded[32:].decode()

    def save(self, *args, **kwargs):
        if not self.pk:  # Only encrypt on creation
            self.password_encrypted = self.encrypt_password(self.password_encrypted)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Password")
        verbose_name_plural = _("Passwords")


class OTPCode(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
