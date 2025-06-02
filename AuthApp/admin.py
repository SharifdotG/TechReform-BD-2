"""
Django admin configuration for the AuthApp.

This module defines the admin interface configuration for authentication-related models.
It provides customized admin panels for managing user profiles with enhanced functionality
including filtering, searching, and organized field layouts.

Classes:
    UserProfileAdmin: Custom admin configuration for UserProfile model
"""

from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Django admin configuration for UserProfile model.

    This admin class provides a comprehensive interface for managing user profiles
    in the Django admin panel. It includes customized display options, filtering,
    searching capabilities, and organized field groupings.

    Attributes:
        list_display (tuple): Fields displayed in the admin list view
        list_filter (tuple): Fields available for filtering in the sidebar
        search_fields (tuple): Fields that can be searched in the admin
        readonly_fields (tuple): Fields that cannot be edited in the admin
        fieldsets (tuple): Organized grouping of fields in the detail view
    """

    list_display = ("user", "role", "phone", "is_verified", "created_at")
    list_filter = ("role", "is_verified")
    search_fields = ("user__username", "user__email", "phone", "address")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("User Information", {"fields": ("user", "role", "phone", "address")}),
        ("Profile Image", {"fields": ("profile_image",)}),
        ("Status", {"fields": ("is_verified",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
