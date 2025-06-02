"""URL patterns for the CompareApp module.

This module defines URL routing for the product comparison functionality
in the TechReform application. It provides endpoints for users to add
products to their comparison list, view the comparison, remove items,
and clear the entire comparison list.

The URL patterns handle:
- Adding products to comparison
- Viewing the comparison list
- Removing individual products from comparison
- Clearing all products from comparison

All views are imported from the CompareApp.views module.
"""

from django.urls import path
from . import views

urlpatterns = [
    path("add/", views.add_to_compare, name="add_to_compare"),
    path("view/", views.view_compare_list, name="view_compare_list"),
    path("remove/", views.remove_from_compare, name="remove_from_compare"),
    path("clear/", views.clear_compare_list, name="clear_compare_list"),
]
