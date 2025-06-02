"""
Django application configuration for the Authentication App.

This module contains the Django app configuration for the AuthApp, which is responsible
for handling all authentication-related functionality in the TechReform application.
The app manages user registration, login/logout, profile management, and implements
role-based access control throughout the system.

Features provided by this app:
    - User authentication and session management
    - User registration and profile creation
    - Role-based access control with multiple user types
    - Profile image management
    - User verification system

Classes:
    AuthAppConfig: Main configuration class for the AuthApp Django application
"""

from django.apps import AppConfig


class AuthAppConfig(AppConfig):
    """
    Django application configuration for the AuthApp.

    This class configures the Authentication application which handles user
    authentication, registration, login/logout functionality, and user profile
    management. The app provides comprehensive user management features including
    role-based access control and user profile customization.

    Attributes:
        default_auto_field (str): Specifies the default primary key field type
        name (str): The Python path to the application
        verbose_name (str): Human-readable name for the app in Django admin
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "AuthApp"
    verbose_name = "Authentication & User Management"
