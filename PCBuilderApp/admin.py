"""
Django admin configuration for the PCBuilderApp.

This module registers the PCBuilder and PCBuilderItem models with the Django admin
interface, providing administrators with a web-based interface to manage PC
configurations and their components.

The admin interface allows administrators to:
- View and manage PC build configurations
- Monitor user-created builds and their components
- Handle public/private build visibility settings
- Track build creation and modification timestamps
- Manage individual PC components and their associations
"""

from django.contrib import admin
from .models import PCBuilder, PCBuilderItem


@admin.register(PCBuilder)
class PCBuilderAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for PCBuilder model.

    Provides comprehensive management capabilities for PC build configurations,
    including filtering, searching, and bulk operations for administrators.
    """

    list_display = ('name', 'user', 'is_public', 'get_item_count', 'get_total_price', 'created_at', 'updated_at')
    list_filter = ('is_public', 'created_at', 'updated_at')
    search_fields = ('name', 'user__username', 'user__email')
    readonly_fields = ('id', 'created_at', 'updated_at', 'get_total_price', 'get_item_count', 'get_recommended_wattage', 'is_complete')
    ordering = ('-created_at',)

    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'name', 'user', 'session_id')
        }),
        ('Configuration', {
            'fields': ('is_public',)
        }),
        ('Calculated Properties', {
            'fields': ('get_total_price', 'get_item_count', 'get_recommended_wattage', 'is_complete'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PCBuilderItem)
class PCBuilderItemAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for PCBuilderItem model.

    Manages individual PC components within builds, allowing administrators
    to view and modify component assignments, prices, and technical specifications.
    """

    list_display = ('pc_builder', 'component_type', 'product_name', 'product_price', 'product_tdp')
    list_filter = ('component_type', 'pc_builder__is_public')
    search_fields = ('product_name', 'pc_builder__name', 'pc_builder__user__username')
    readonly_fields = ('id',)
    ordering = ('pc_builder', 'component_type')

    fieldsets = (
        ('Component Information', {
            'fields': ('id', 'pc_builder', 'component_type')
        }),
        ('Product Details', {
            'fields': ('product_id', 'product_name', 'product_price', 'product_tdp')
        }),
    )
