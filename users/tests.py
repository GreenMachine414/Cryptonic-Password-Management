"""Tests for `users` app."""

from http import HTTPStatus

import pytest
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized

from users.models import CustomUser, Password


class UserManagerTestCase(TestCase):
    """Test for `CustomUserManager` class."""

    def test_create_normal(self):
        """Test `create_user()`.

        Tests if `create_user()` creates a `CustomUser` model object.
        Tests if the `__str__()` of `CustomUser` returns the username.

        """
        user = CustomUser.objects.create_user(
            username="jdoe", email="jdoe@gmail.com", password="password123"
        )
        self.assertTrue(isinstance(user, CustomUser))
        self.assertEqual(str(user), "jdoe")  # Check for username instead of email

    def test_create_user_email_none_raises_value_error(self):
        """Test `create_user()`.

        Tests if `create_user()` raises `ValueError` when the `username` is `None`.

        """
        with pytest.raises(ValueError) as exc_info:
            CustomUser.objects.create_user(username=None, email=None, password=None)
        self.assertEqual(exc_info.type, ValueError)

    def test_create_superuser(self):
        """Test `create_superuser()`.

        Tests if `create_superuser()` creates a `CustomUser` model object.
        Tests if the `__str__()` of `CustomUser` returns the username.

        """
        user = CustomUser.objects.create_superuser(
            username="jdoe", email="jdoe@gmail.com", password="password123"
        )
        self.assertTrue(isinstance(user, CustomUser))
        self.assertEqual(str(user), "jdoe")  # Check for username instead of email

    def test_create_superuser_raises_value_error_is_staff_false(self):
        """Test for `create_superuser()`.

        Tests if `create_superuser()` raises `ValueError` when `is_staff` argument
        to the function is set `False`.

        """
        with pytest.raises(ValueError) as exc_info:
            CustomUser.objects.create_superuser(
                username="jdoe",
                email="jdoe1@gmail.com",
                password="password123",
                is_staff=False,
            )
        self.assertEqual(exc_info.type, ValueError)

    def test_create_superuser_raises_value_error_is_superuser_false(self):
        """Test for `create_superuser()`.

        Tests if `create_superuser()` raises `ValueError` when `is_superuser` argument
        to the function is set `False`.

        """
        with pytest.raises(ValueError) as exc_info:
            CustomUser.objects.create_superuser(
                username="jdoe",
                email="jdoe1@gmail.com",
                password="password123",
                is_superuser=False,
            )
        self.assertEqual(exc_info.type, ValueError)


class CustomUserTestCase(TestCase):
    """Tests for `CustomUser` model."""

    def test_create(self):
        """Tests if `CustomUser`'s `create()` method is working using a query."""
        user = CustomUser.objects.create(
            username="jdoe", email="jdoe@gmail.com", password="password123"
        )
        query = CustomUser.objects.get(username="jdoe")  # Query by username
        self.assertEqual(user, query)

    def test_create_user_raises_not_unique_integrity_error_with_same_username(self):
        """Tests if `CustomUser`'s `create()` method raises an `IntegrityError` for duplicate usernames."""
        CustomUser.objects.create(username="jdoe", email="jdoe@gmail.com", password="password123")

        with pytest.raises(IntegrityError) as exc_info:
            CustomUser.objects.create(
                username="jdoe", email="jdoe1@gmail.com", password="password123"
            )
        self.assertEqual(exc_info.type, IntegrityError)


class SignUpViewTestCase(TestCase):
    """Tests for `SignUpView` view."""

    @parameterized.expand(
        [
            (
                {
                    "first_name": "john",
                    "last_name": "doe",
                    "username": "jdoe",  # Test with username as the identifier
                    "email": "jdoe@gmail.com",
                    "password1": "p@$$W0RDL@rG3",
                    "password2": "p@$$W0RDL@rG3",
                },
                HTTPStatus.FOUND,
            ),
            (
                {
                    "first_name": "john",
                    "last_name": "doe",
                    "username": "jdoe",  # Test with username as the identifier
                    "email": "jdoe@gmail.com",
                    "password1": "password",
                    "password2": "password",
                },
                HTTPStatus.OK,
            ),
        ]
    )
    def test_signup_view(self, params, status_code):
        """Test `SignUpView` with strong and weak passwords.

        Tests if registration is successful for strong passwords.
        Tests if registration fails for weak passwords.

        """
        signup_url = reverse("users:signup")
        response = self.client.post(signup_url, data=params)
        self.assertEqual(response.status_code, status_code)


class LoginTestCase(TestCase):
    """Tests for Django's built-in `Login` view."""

    def setUp(self):
        """Set up test data for the class."""
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")

        self.login_params = {"username": "jdoe", "password": "p@$$W0RDL@rG3"}
        CustomUser.objects.create_user(
            username="jdoe", email="jdoe@gmail.com", password="p@$$W0RDL@rG3"
        )

    def test_signinview(self):
        """Test `SignUpView`, it should redirect."""
        response = self.client.post(self.login_url, data=self.login_params)
        # redirects after a successful login
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        response = self.client.get(reverse("home"))
        self.assertEqual(str(response.context.get("user")), "jdoe")  # Check for username

    def test_logged_in_user_sees_correct_template(self):
        """Test if logged in user sees the password change page."""
        response = self.client.login(username="jdoe", password="p@$$W0RDL@rG3")
        response = self.client.get(reverse("password_change"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "registration/password_change.html")

    def test_signinview_invalid_user_password(self):
        """Test login by providing invalid user credentials."""
        response = self.client.post(
            self.login_url, data={"username": "jdoe", "password": "password"}
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "registration/login.html")
        self.assertTrue("errors" in response.context)
        self.assertTrue(
            "Please enter a correct username and password" in str(response.context.get("errors"))
        )
        self.assertEqual(str(response.context.get("user")), "AnonymousUser")


class BasePasswordTest(TestCase):
    def setUp(self):
        """Set up the user and password instance for all password tests."""
        # Create a custom user
        self.user = get_user_model().objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword123"
        )

        # Create a password object associated with the user
        self.password = Password.objects.create(
            user=self.user,
            username="user1",
            website="example.com",
            website_username="testuser_example",
            password_encrypted="encryptedpassword123",
        )


class PasswordModelTest(BasePasswordTest):
    def test_password_creation(self):
        """Test password object creation."""
        self.assertEqual(self.password.user, self.user)
        self.assertEqual(self.password.username, "user1")
        self.assertEqual(self.password.website, "example.com")
        self.assertEqual(self.password.website_username, "testuser_example")
        self.assertEqual(self.password.password_encrypted, "encryptedpassword123")
        self.assertIsNotNone(self.password.created)

    def test_password_update(self):
        """Test updating the password fields."""
        self.password.username = "newuser"
        self.password.website = "newexample.com"
        self.password.website_username = "newuser_example"
        self.password.password_encrypted = "newencryptedpassword123"
        self.password.save()

        updated_password = Password.objects.get(pk=self.password.pk)
        self.assertEqual(updated_password.username, "newuser")
        self.assertEqual(updated_password.website, "newexample.com")
        self.assertEqual(updated_password.website_username, "newuser_example")
        self.assertEqual(updated_password.password_encrypted, "newencryptedpassword123")

    def test_password_deletion(self):
        """Test deleting a password."""
        password_id = self.password.pk
        self.password.delete()

        # Ensure the password is deleted from the database
        with self.assertRaises(Password.DoesNotExist):
            Password.objects.get(pk=password_id)

    def test_insert_multiple_passwords(self):
        """Test inserting multiple passwords for the same user."""
        # Create additional passwords for the user
        self.user.passwords.create(
            username="user2",
            website="another.com",
            website_username="user2_example",
            password_encrypted="encryptedpassword456",
        )
        self.user.passwords.create(
            username="user3",
            website="third.com",
            website_username="user3_example",
            password_encrypted="encryptedpassword789",
        )

        # Retrieve all passwords for the user
        passwords = self.user.passwords.all()

        self.assertEqual(passwords.count(), 3)  # 3 passwords should be associated with the user
        self.assertIn(self.password, passwords)
        self.assertEqual(passwords.filter(username="user2").count(), 1)
        self.assertEqual(passwords.filter(username="user3").count(), 1)

    def test_custom_user_password_relationship(self):
        """Test the expected relationship between CustomUser and Password models (1 to many)."""
        # Check that the user has associated Password objects
        user_passwords = self.user.passwords.all()  # Use the 'passwords' related name

        # Ensure the user has the expected number of passwords
        self.assertEqual(
            user_passwords.count(), 1
        )  # Only one password should be associated with this user

        # Ensure the correct password is associated with the user
        self.assertIn(self.password, user_passwords)


class PasswordListViewTest(TestCase):
    def setUp(self):
        """Set up the user and password instance for all password list view tests."""
        # Create a custom user
        self.user = get_user_model().objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword123"
        )

        # Create a password object associated with the user
        self.password = Password.objects.create(
            user=self.user,
            username="user1",
            website="example.com",
            website_username="testuser_example",
            password_encrypted="encryptedpassword123",
        )

        self.url = reverse("users:password-list")  # Adjust to your actual URL name

    def test_empty_password_list(self):
        """Test that the password list view returns empty when the user has no passwords."""
        self.user.passwords.all().delete()  # Remove the user's passwords

        self.client.login(username="testuser", password="testpassword123")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "password_list.html")

        passwords = response.context["passwords"]
        self.assertEqual(len(passwords), 0)  # No passwords for this user

    def test_single_password_in_list(self):
        """Test that the password list view shows only one password."""
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "password_list.html")

        passwords = response.context["passwords"]
        self.assertEqual(len(passwords), 1)  # One password should be displayed
        self.assertIn(self.password, passwords)

    def test_multiple_passwords_in_list(self):
        """Test that the password list view shows multiple passwords."""
        # Create additional passwords for the user
        self.user.passwords.create(
            username="user2",
            website="another.com",
            website_username="user2_example",
            password_encrypted="encryptedpassword456",
        )
        self.user.passwords.create(
            username="user3",
            website="third.com",
            website_username="user3_example",
            password_encrypted="encryptedpassword789",
        )

        self.client.login(username="testuser", password="testpassword123")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "password_list.html")

        passwords = response.context["passwords"]
        self.assertEqual(len(passwords), 3)  # Three passwords should be associated with this user

    def test_list_view_navigation_to_detail_view(self):
        """Test that clicking on a password redirects to the password detail view."""
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.get(self.url)

        # Find the URL for the first password detail view (assuming it's correct in the template)
        password_detail_url = reverse("users:password-detail", kwargs={"pk": self.password.pk})

        # Check if the detail view link is in the response context
        self.assertContains(response, password_detail_url)

        # Test that clicking the detail link redirects to the correct page
        detail_response = self.client.get(password_detail_url)
        self.assertEqual(detail_response.status_code, 200)
        self.assertTemplateUsed(detail_response, "password_details.html")

    def test_password_list_view_rbac_authenticated_user(self):
        """Test that an authenticated user can view the password list."""
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "password_list.html")

    def test_password_list_view_rbac_anonymous_user(self):
        """Test that an anonymous user is redirected to the login page."""
        response = self.client.get(self.url)

        # Expect a redirect to the login page
        self.assertRedirects(response, "/accounts/login/")

    def test_password_list_view_rbac_other_user(self):
        """Test that one user cannot access another user's password list."""
        # Create another user
        other_user = get_user_model().objects.create_user(
            username="otheruser", email="otheruser@example.com", password="otherpassword123"
        )

        # Create a password for the other user
        other_user.passwords.create(
            username="user4",
            website="fourth.com",
            website_username="user4_example",
            password_encrypted="encryptedpassword123",
        )

        # Login as the first user
        self.client.login(username="testuser", password="testpassword123")

        # Ensure the second user's password is not in the response
        response = self.client.get(self.url)
        self.assertNotIn(other_user.passwords.first(), response.context["passwords"])

        # Ensure the first user's password is present
        self.assertIn(self.password, response.context["passwords"])


class PasswordDetailViewTest(BasePasswordTest):
    def setUp(self):
        super().setUp()  # Ensure the common user and password are set up

        # URL for the detail view (assuming you have a named URL pattern for password detail)
        self.url = reverse("users:password-detail", kwargs={"pk": self.password.pk})

    def test_password_detail_view_for_authenticated_user(self):
        """Test that an authenticated user can view the password detail page."""
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.get(self.url)

        # Check that the status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Ensure the correct template is used
        self.assertTemplateUsed(response, "password_details.html")

        # Check that the password object is in the context
        self.assertEqual(response.context["password"], self.password)

    def test_password_detail_view_for_anonymous_user(self):
        """Test that an anonymous user is redirected to the login page."""
        response = self.client.get(self.url)

        # Check if the user is redirected to the login page
        self.assertRedirects(response, "/accounts/login/")


class PasswordUpdateDeleteViewTest(BasePasswordTest):
    def setUp(self):
        super().setUp()  # Ensure the common user and password are set up

        # URLs for update and delete views
        self.update_url = reverse("users:update-password", kwargs={"pk": self.password.pk})
        self.delete_url = reverse("users:delete-password", kwargs={"pk": self.password.pk})

    def test_password_update_view_for_authenticated_user(self):
        self.client.login(username="testuser", password="testpassword123")

        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)  # Check that the user can access the page

    def test_password_update_view_for_anonymous_user(self):
        response = self.client.get(self.update_url)
        self.assertRedirects(response, "/accounts/login/")

    def test_password_delete_view_for_authenticated_user(self):
        self.client.login(username="testuser", password="testpassword123")

        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)  # Check that the user can access the page

    def test_password_delete_view_for_anonymous_user(self):
        response = self.client.get(self.delete_url)
        self.assertRedirects(response, "/accounts/login/")
