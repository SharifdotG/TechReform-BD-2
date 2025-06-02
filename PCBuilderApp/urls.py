"""
URL routing configuration for the PC Builder application.

This module defines URL patterns for the PC Builder functionality,
which allows users to build custom PC configurations by selecting
components and managing their saved builds.

The URL patterns include:
- PC builder interface and component selection
- Build management (save, load, delete, clear)
- Cart integration for purchasing builds
- PDF export functionality for build specifications

All views are implemented in the corresponding views.py module.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Main PC builder interface
    path("", views.pc_builder, name="pc_builder"),
    # Build management operations
    path("clear/", views.clear_build, name="clear_build"),
    # Component selection routes
    # Note: Storage route must be before the generic component route to avoid conflicts
    path("select/storage/", views.select_storage, name="select_storage"),
    path(
        "select/<str:component_type>/", views.select_component, name="select_component"
    ),
    # Component addition and removal
    path("add/", views.add_component_to_build, name="add_component_to_build"),
    path(
        "remove/<str:component_type>/",
        views.remove_component_from_build,
        name="remove_component_from_build",
    ),
    # Saved builds management
    path("save/", views.save_pc_build, name="save_pc_build"),
    path("my-builds/", views.my_saved_builds, name="my_saved_builds"),
    path("load/<uuid:build_id>/", views.load_saved_build, name="load_saved_build"),
    path(
        "delete/<uuid:build_id>/", views.delete_saved_build, name="delete_saved_build"
    ),
    # Cart integration
    path("add-to-cart/", views.add_build_to_cart, name="add_build_to_cart"),
    path(
        "add-to-cart/<uuid:build_id>/",
        views.add_build_to_cart,
        name="add_saved_build_to_cart",
    ),
    # PDF export functionality
    path("export-pdf/", views.export_build_pdf, name="export_build_pdf"),
    path(
        "export-pdf/<uuid:build_id>/",
        views.export_build_pdf,
        name="export_saved_build_pdf",
    ),
]
