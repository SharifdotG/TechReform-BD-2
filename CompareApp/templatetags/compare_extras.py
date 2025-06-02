"""
Django template filters for product comparison functionality.

This module provides custom template filters specifically designed for the
product comparison feature in the TechReform e-commerce application. The
filters enable dynamic attribute access in templates, which is essential
for comparing products with varying specifications and attributes.

Available Filters:
    - getattribute: Dynamically access object attributes in templates

These filters are particularly useful when displaying comparison tables
where product attributes need to be accessed dynamically based on field
names or user selections.
"""

from django import template

register = template.Library()


@register.filter
def getattribute(obj, attr):
    """
    Custom template filter to get an attribute of an object dynamically.
    Usage: {{ object|getattribute:attribute_name }}
    """
    try:
        return getattr(obj, attr)
    except (AttributeError, TypeError):
        return None
