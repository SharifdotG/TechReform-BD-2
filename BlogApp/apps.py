"""Django application configuration for the BlogApp.

This module contains the Django app configuration for the blog functionality
of the TechReform application. It defines the app-specific settings and
metadata required for Django to properly initialize and manage the blog
application.

The BlogApp provides comprehensive blog functionality including:
- Blog post creation and management
- Category and tag organization
- Comment system with moderation
- Featured posts highlighting
- SEO-friendly URL slugs
"""

from django.apps import AppConfig


class BlogappConfig(AppConfig):
    """Django application configuration class for BlogApp.

    This class defines the configuration settings for the BlogApp Django
    application. It inherits from Django's AppConfig and sets up the
    necessary metadata for the blog functionality.

    Attributes:
        default_auto_field (str): Specifies the default primary key field
            type for models in this app. Set to BigAutoField for better
            performance with large datasets.
        name (str): The Python path to the application module. Used by
            Django to identify and load the app.

    The BlogApp provides a complete blogging solution with features for
    content management, categorization, tagging, and user engagement
    through comments.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "BlogApp"
