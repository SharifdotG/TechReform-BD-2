"""
URL configuration for WishlistApp.

This module defines the URL patterns for the WishlistApp, mapping URLs
to their corresponding view functions. It handles all wishlist-related
operations including adding items, viewing the wishlist, removing items,
and clearing the entire wishlist.

URL Patterns:
    - add/: Add a product to the wishlist
    - view/: Display the current user's wishlist
    - remove/: Remove a specific item from the wishlist
    - clear/: Remove all items from the wishlist
"""

from django.urls import path
from . import views

urlpatterns = [
    path("add/", views.add_to_wishlist, name="add_to_wishlist"),
    path("view/", views.view_wishlist, name="view_wishlist"),
    path("remove/", views.remove_from_wishlist, name="remove_from_wishlist"),
    path("clear/", views.clear_wishlist, name="clear_wishlist"),
]
