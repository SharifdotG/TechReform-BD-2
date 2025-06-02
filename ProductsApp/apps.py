"""
ProductsApp Django Application Configuration.

This module contains the Django application configuration for the ProductsApp,
which handles product management functionality within the TechReform application.
The ProductsApp is responsible for managing technology products including
CPUs, GPUs, motherboards, RAM, storage devices, and other computer components.
"""

from django.apps import AppConfig


class ProductsappConfig(AppConfig):
    """
    Django application configuration for ProductsApp.

    This class configures the ProductsApp Django application, setting up
    the necessary configuration parameters for the products management system.
    The app handles product catalog functionality, product details, categories,
    specifications, and related product operations.

    Attributes:
        default_auto_field (str): Specifies the default primary key field type
            for models in this app. Uses BigAutoField for scalability.
        name (str): The Python path to the application module.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "ProductsApp"
