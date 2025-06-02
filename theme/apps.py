"""
Django application configuration for the Theme app.

This module contains the Django app configuration for the Theme application,
which handles the user interface styling and static assets for the TechReform
application. The Theme app manages Tailwind CSS integration, custom styling,
and responsive design components.

The Theme app provides:
    - Tailwind CSS compilation and optimization
    - Custom CSS and JavaScript assets
    - Responsive design templates and components
    - UI consistency across the application
    - Static file management and optimization
"""

from django.apps import AppConfig


class ThemeConfig(AppConfig):
    name = "theme"
