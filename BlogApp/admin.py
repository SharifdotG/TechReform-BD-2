"""Django admin configuration for the BlogApp.

This module contains Django admin interface configurations for blog-related models
including categories, tags, blog posts, and comments. It provides customized admin
interfaces with enhanced functionality for content management.

The admin configurations include:
- CategoryAdmin: Management interface for blog categories
- TagAdmin: Management interface for blog tags
- BlogPostAdmin: Comprehensive management interface for blog posts
- CommentAdmin: Management interface for blog comments

Each admin class is configured with appropriate list displays, filters, search
functionality, and fieldsets to provide an optimal content management experience.
"""

from django.contrib import admin
from .models import Category, BlogPost, Comment, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Django admin configuration for Category model.

    Provides admin interface for managing blog categories with enhanced
    functionality including search capabilities and automatic slug generation.

    Features:
    - Display of name, slug, and creation date in list view
    - Search functionality by category name
    - Automatic slug generation from category name
    """

    list_display = ("name", "slug", "created_at")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Django admin configuration for Tag model.

    Provides admin interface for managing blog tags with search functionality
    and automatic slug generation to ensure SEO-friendly URLs.

    Features:
    - Display of tag name and slug in list view
    - Search functionality by tag name
    - Automatic slug generation from tag name
    """

    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    """Django admin configuration for BlogPost model.

    Comprehensive admin interface for managing blog posts with advanced features
    including filtering, searching, bulk editing, and organized fieldsets.

    Features:
    - Detailed list view with key post information
    - Advanced filtering by status, featured status, category, and date
    - Comprehensive search across title, summary, and content
    - Automatic slug generation from post title
    - Raw ID fields for efficient foreign key selection
    - Date hierarchy for easy navigation
    - Horizontal filter for tag selection
    - Inline editing of status and featured flags
    - Read-only view count field
    - Organized fieldsets for better content editing experience
    """

    list_display = (
        "title",
        "author",
        "category",
        "status",
        "is_featured",
        "created_at",
        "view_count",
    )
    list_filter = ("status", "is_featured", "category", "created_at")
    search_fields = ("title", "summary", "content")
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ("author",)
    date_hierarchy = "created_at"
    filter_horizontal = ("tags",)
    list_editable = ("status", "is_featured")
    readonly_fields = ("view_count",)
    fieldsets = (
        (
            "Post Information",
            {"fields": ("title", "slug", "author", "category", "tags")},
        ),
        ("Content", {"fields": ("featured_image", "summary", "content")}),
        ("Publication", {"fields": ("status", "is_featured", "published_at")}),
        ("Statistics", {"fields": ("view_count",)}),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Django admin configuration for Comment model.

    Provides admin interface for managing blog comments with moderation
    capabilities and efficient filtering and searching functionality.

    Features:
    - Display of comment author, associated post, date, and approval status
    - Filtering by approval status and creation date
    - Search across comment content, author username, and post title
    - Inline editing of approval status for quick moderation
    - Raw ID fields for efficient foreign key selection
    """

    list_display = ("author", "post", "created_at", "is_approved")
    list_filter = ("is_approved", "created_at")
    search_fields = ("content", "author__username", "post__title")
    list_editable = ("is_approved",)
    raw_id_fields = ("post", "author")
