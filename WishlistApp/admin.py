"""
Django admin configuration for WishlistApp.

This module defines the admin interface configurations for WishList and WishlistItem
models, providing administrative functionality for managing user wishlists and
wishlist items through Django's admin panel.
"""

from django.contrib import admin
from .models import WishList, WishlistItem


class WishlistItemInline(admin.TabularInline):
    """
    Inline admin configuration for WishlistItem model.

    Provides a tabular inline interface for managing wishlist items directly
    within the WishList admin page. This allows administrators to view and
    edit wishlist items without navigating to a separate page.

    Attributes:
        model: The WishlistItem model to be displayed inline.
        extra: Number of extra empty forms to display (0 for no extras).
        readonly_fields: Fields that cannot be edited in the admin interface.
    """
    model = WishlistItem
    extra = 0
    readonly_fields = ('product_id', 'category', 'date_added')

@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    """
    Admin configuration for WishList model.

    Provides administrative interface for managing user wishlists with enhanced
    display options, filtering, and search capabilities. Includes inline editing
    of wishlist items for convenient management.

    Attributes:
        list_display: Fields to display in the admin list view.
        list_filter: Fields available for filtering the list view.
        search_fields: Fields that can be searched in the admin interface.
        inlines: Inline admin configurations included in this admin page.
    """
    list_display = ('__str__', 'user', 'session_id', 'created_at', 'get_wishlist_items_count')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'session_id')
    inlines = [WishlistItemInline]

@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for WishlistItem model.

    Provides administrative interface for managing individual wishlist items
    with comprehensive display, filtering, and search functionality. Includes
    readonly fields to maintain data integrity for automatically generated values.

    Attributes:
        list_display: Fields to display in the admin list view, including
                     relationships and computed values.
        list_filter: Fields available for filtering items by category and date.
        search_fields: Fields that can be searched, including related user data.
        readonly_fields: Fields that cannot be modified to preserve data integrity.
    """
    list_display = ('__str__', 'wishlist', 'user', 'product_id', 'category', 'date_added')
    list_filter = ('category', 'date_added')
    search_fields = ('product_id', 'category', 'user__username')
    readonly_fields = ('date_added',)
