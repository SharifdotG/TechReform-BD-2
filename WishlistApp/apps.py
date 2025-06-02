"""
Django app configuration for WishlistApp.

This module contains the application configuration for the WishlistApp,
which handles user wishlist functionality in the TechReform application.
"""

from django.apps import AppConfig


class WishlistappConfig(AppConfig):
    """
    Configuration class for the WishlistApp Django application.

    This class defines the configuration settings for the WishlistApp,
    including the default auto field type and the application name.
    The WishlistApp manages user wishlists for products in the e-commerce
    platform, supporting both authenticated and anonymous users.

    Attributes:
        default_auto_field (str): The default field type for auto-generated
            primary keys in models.
        name (str): The full Python path to the application.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "WishlistApp"
