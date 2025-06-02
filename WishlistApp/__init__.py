"""
WishlistApp - Django application for managing user wishlists.

This package provides comprehensive wishlist functionality for the TechReform
e-commerce platform. It supports both authenticated users and anonymous
visitors through session-based storage, allowing users to save products
for later purchase or comparison.

Key Features:
    - User-based wishlists for authenticated users
    - Session-based wishlists for anonymous visitors
    - Support for multiple product categories
    - AJAX-enabled wishlist operations
    - Admin interface for wishlist management
    - Context processors for template integration

Components:
    models: Database models for WishList and WishlistItem
    views: View functions for wishlist operations
    admin: Django admin configuration
    urls: URL routing configuration
    context_processors: Template context providers

The application integrates seamlessly with Django's authentication system
and provides a smooth user experience for managing product wishlists
across the entire e-commerce platform.
"""
