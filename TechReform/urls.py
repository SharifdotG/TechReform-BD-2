"""
Main URL configuration for TechReform e-commerce platform.

This module defines the root URL routing for the TechReform project, organizing
all application URLs into a hierarchical structure. The configuration routes
incoming HTTP requests to appropriate Django applications based on URL patterns.

URL Structure Overview:
    /                   - ProductsApp: Homepage, catalog, product details, search
    /admin/             - Django Admin: Administrative interface
    /auth/              - AuthApp: Authentication, user management, support
    /cart/              - CartApp: Shopping cart, checkout, order management
    /pc-builder/        - PCBuilderApp: Custom PC configuration tool
    /compare/           - CompareApp: Product comparison functionality
    /wishlist/          - WishlistApp: User wishlists and favorites
    /blog/              - BlogApp: Content management and blog posts
    /ckeditor/          - CKEditor: Rich text editor file uploads

Application Routing:
    Each application maintains its own urls.py file with detailed URL patterns.
    This promotes modularity and separation of concerns across the platform.

Static File Serving:
    Development-only static file serving is configured for:
    - MEDIA_URL: User-uploaded files (product images, avatars, attachments)
    - STATIC_URL: CSS, JavaScript, and static assets

Security Considerations:
    - Admin interface requires staff-level authentication
    - Authentication URLs handle secure login/logout processes
    - File upload URLs include security validation
    - CSRF protection enabled across all forms

Development Features:
    - Browser auto-reload enabled for development efficiency
    - Debug-friendly URL patterns and error handling

For detailed URL patterns within each application, refer to:
    - ProductsApp/urls.py: Product catalog and search functionality
    - AuthApp/urls.py: User authentication and customer support
    - CartApp/urls.py: Shopping cart and checkout processes
    - PCBuilderApp/urls.py: PC configuration and compatibility
    - CompareApp/urls.py: Product comparison features
    - WishlistApp/urls.py: User wishlist management
    - BlogApp/urls.py: Content and blog management

For more information on Django URL routing, see:
https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""

# =============================================================================
# IMPORTS
# =============================================================================

from django.conf import settings
from django.conf.urls.static import static  # Static file serving for development
from django.contrib import admin  # Django admin interface
from django.urls import path, include  # URL routing utilities


# =============================================================================
# URL PATTERNS CONFIGURATION
# =============================================================================
# Main URL routing configuration for the TechReform e-commerce platform.
# URLs are organized by application functionality with clear separation of concerns.

urlpatterns = (
    [
        # =================================================================
        # ADMINISTRATION
        # =================================================================
        # Django Admin Interface - Requires staff/superuser permissions
        # Provides content management for products, users, orders, and system data
        path("admin/", admin.site.urls),
        # =================================================================
        # DEVELOPMENT TOOLS
        # =================================================================
        # Browser Auto-Reload - Development only feature
        # Automatically refreshes browser when source files change
        path("__reload__/", include("django_browser_reload.urls")),
        # =================================================================
        # CORE E-COMMERCE FUNCTIONALITY
        # =================================================================
        # Homepage and Product Catalog - Root URL handling
        # Includes: homepage, product listing, search, categories, product details
        path("", include("ProductsApp.urls")),
        # Shopping Cart and Checkout System
        # Includes: cart management, checkout process, order history, payment
        path("cart/", include("CartApp.urls")),
        # =================================================================
        # USER MANAGEMENT AND SUPPORT
        # =================================================================
        # Authentication and User Management
        # Includes: login/logout, registration, profile management, user roles,
        # customer support ticket system, password reset functionality
        path("auth/", include("AuthApp.urls")),
        # =================================================================
        # SPECIALIZED TOOLS AND FEATURES
        # =================================================================
        # PC Builder Configuration Tool
        # Includes: component selection, compatibility checking, custom builds,
        # saved configurations, build recommendations
        path("pc-builder/", include("PCBuilderApp.urls")),
        # Product Comparison System
        # Includes: side-by-side comparisons, specification tables,
        # comparison lists, feature analysis
        path("compare/", include("CompareApp.urls")),
        # User Wishlist Management
        # Includes: wishlist creation, product favorites, wishlist sharing,
        # price tracking, availability notifications
        path("wishlist/", include("WishlistApp.urls")),
        # =================================================================
        # CONTENT MANAGEMENT
        # =================================================================
        # Blog and Content System
        # Includes: blog posts, categories, author management, comments,
        # tech articles, product reviews, company news
        path("blog/", include("BlogApp.urls")),
        # Rich Text Editor File Management
        # Handles file uploads for CKEditor including images, documents,
        # and other media files used in blog content and descriptions
        path("ckeditor/", include("ckeditor_uploader.urls")),
    ]
    # =================================================================
    # STATIC FILE SERVING (DEVELOPMENT ONLY)
    # =================================================================
    # Media files: User uploads, product images, profile pictures, attachments
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Static files: CSS, JavaScript, fonts, and other static assets
    # Note: In production, these should be served by a web server (nginx/apache)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
