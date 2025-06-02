"""Django admin configuration for CompareApp models.

This module configures the Django admin interface for product comparison
functionality. It provides comprehensive admin panels for managing comparison
lists and individual comparison items with enhanced usability and filtering.

Features:
- Inline editing of comparison items within comparison lists
- Advanced filtering by date, category, and user
- Search functionality across multiple fields
- Read-only protection for sensitive fields
- Comprehensive list displays with relevant information

Admin Classes:
- CompareListAdmin: Management interface for comparison lists
- CompareItemAdmin: Management interface for individual comparison items
- CompareItemInline: Inline editor for comparison items

The admin interface enables staff to:
- Monitor user comparison activity and patterns
- Debug comparison-related issues
- Manage comparison data for customer support
- Analyze product comparison trends

Usage:
Access through Django admin at /admin/ with appropriate permissions.
"""

from django.contrib import admin
from .models import CompareList, CompareItem


class CompareItemInline(admin.TabularInline):
    """Inline admin interface for CompareItem model.

    Allows editing comparison items directly within the comparison list
    admin page. Provides a streamlined interface for viewing and managing
    all items within a specific comparison list.

    Configuration:
        - No extra empty forms displayed by default
        - Key fields set as read-only to prevent data corruption
        - Displays product ID, category, and addition date
    """
    model = CompareItem
    extra = 0
    readonly_fields = ("product_id", "category", "date_added")


@admin.register(CompareList)
class CompareListAdmin(admin.ModelAdmin):
    """Admin interface for CompareList model.

    Provides comprehensive management of user comparison lists with
    detailed information display and advanced filtering capabilities.
    Includes inline editing of comparison items for efficient management.

    Features:
        - Displays user information, session ID, and creation date
        - Shows item count for each comparison list
        - Filtering by creation date for temporal analysis
        - Search by username and session ID
        - Inline editing of comparison items

    List Display:
        - String representation of the list
        - Associated user (if authenticated)
        - Session ID (for anonymous users)
        - Creation timestamp
        - Number of items in the list
    """
    list_display = (
        "__str__",
        "user",
        "session_id",
        "created_at",
        "get_compare_items_count",
    )
    list_filter = ("created_at",)
    search_fields = ("user__username", "session_id")
    inlines = [CompareItemInline]


@admin.register(CompareItem)
class CompareItemAdmin(admin.ModelAdmin):
    """Admin interface for CompareItem model.

    Provides detailed management of individual comparison items with
    comprehensive filtering and search capabilities. Enables staff to
    monitor and manage specific products in user comparison lists.

    Features:
        - Complete item information display
        - Filtering by product category and date added
        - Search across product ID, category, and username
        - Read-only date field to preserve historical data

    List Display:
        - String representation of the item
        - Associated comparison list
        - Item owner (user)
        - Product ID and category
        - Addition timestamp

    Filtering:
        - By product category for category-specific analysis
        - By date added for temporal trends

    Search:
        - Product ID for direct item lookup
        - Category for category-based searches
        - Username for user-specific item searches
    """
    list_display = (
        "__str__",
        "compare_list",
        "user",
        "product_id",
        "category",
        "date_added",
    )
    list_filter = ("category", "date_added")
    search_fields = ("product_id", "category", "user__username")
    readonly_fields = ("date_added",)
