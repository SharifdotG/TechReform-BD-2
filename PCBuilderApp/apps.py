"""
Django application configuration for PCBuilderApp.

This module contains the application configuration class for the PC Builder
application, which provides functionality for users to build custom PC
configurations by selecting compatible components.
"""

from django.apps import AppConfig


class PcbuilderappConfig(AppConfig):
    """
    Configuration class for the PCBuilderApp Django application.

    This class defines the configuration settings for the PC Builder application,
    which handles the creation and management of custom PC builds. It allows users
    to select and combine various computer components (CPU, GPU, RAM, etc.) to
    create complete PC configurations while checking compatibility between components.

    Attributes:
        default_auto_field (str): Specifies the default primary key field type
            for models in this app. Set to BigAutoField for better performance
            and larger ID ranges.
        name (str): The Python path to the application module. Used by Django
            to identify and load the application.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "PCBuilderApp"
