"""Django app configuration for CompareApp.

This module contains the Django application configuration for the product
comparison functionality of the TechReform e-commerce platform. The CompareApp
enables users to compare products across different categories side-by-side
to make informed purchasing decisions.

The app provides:
- Session-based comparison for anonymous users
- User account integration for registered customers
- Multi-category product comparison capabilities
- Dynamic product model integration with ProductsApp
- Persistent comparison lists across browser sessions

Key Features:
- Unlimited products per comparison list
- Cross-category product comparisons
- Real-time product information updates
- User-friendly comparison interface
- Administrative management tools
"""

from django.apps import AppConfig


class CompareappConfig(AppConfig):
    """Configuration class for the CompareApp Django application.

    Defines the basic configuration settings for the product comparison
    application, including the default auto field type and app name.

    Attributes:
        default_auto_field (str): Default field type for auto-generated primary keys
        name (str): The name of the Django application

    Usage:
        This configuration is automatically loaded by Django when the
        application is included in the INSTALLED_APPS setting.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "CompareApp"
