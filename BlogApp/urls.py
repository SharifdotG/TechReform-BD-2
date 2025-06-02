"""URL configuration for the BlogApp.

This module defines the URL routing patterns for the blog functionality
of the TechReform application. It maps URL paths to their corresponding
view functions and includes namespacing for proper URL organization.

The URL patterns are organized into logical groups:
- Public blog views: Accessible to all visitors for reading content
- Blogger views: Available to authenticated users for content creation
- Content manager views: Admin-level views for content moderation
- Comment actions: User interaction endpoints for commenting

All URLs use descriptive names that can be referenced in templates and
views using Django's reverse URL resolution. Slug-based URLs provide
SEO-friendly paths for content pages.

App namespace: 'blog' - Use as 'blog:url_name' in reverse lookups.
"""

from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    # Public blog views - Accessible to all visitors
    path("", views.blog_list, name="blog_list"),
    # Main blog listing page showing published posts

    path("post/<slug:slug>/", views.post_detail, name="post_detail"),
    # Individual blog post detail page with comments

    path("category/<slug:slug>/", views.category_posts, name="category_posts"),
    # Posts filtered by specific category

    path("tag/<slug:slug>/", views.tag_posts, name="tag_posts"),
    # Posts filtered by specific tag

    path("search/", views.search_posts, name="search_posts"),
    # Search functionality across blog content

    # Blogger views - Authenticated user content management
    path("my-posts/", views.my_posts, name="my_posts"),
    # User's personal post management dashboard

    path("create/", views.create_post, name="create_post"),
    # Create new blog post form

    path("edit/<slug:slug>/", views.edit_post, name="edit_post"),
    # Edit existing blog post (author or admin only)

    path("delete/<slug:slug>/", views.delete_post, name="delete_post"),
    # Delete blog post (author or admin only)

    # Content manager views - Administrative content moderation
    path("pending-posts/", views.pending_posts, name="pending_posts"),
    # List of posts awaiting review/approval

    path("review/<slug:slug>/", views.review_post, name="review_post"),
    # Review and approve/reject pending posts

    path("content-analysis/", views.content_analysis, name="content_analysis"),
    # Analytics dashboard for content performance

    path(
        "content-analysis/export/<str:format>/",
        views.export_content_analysis,
        name="export_content_analysis",
    ),
    # Export content analytics in various formats (PDF, CSV, etc.)

    # Comment actions - User interaction endpoints
    path("post/<slug:slug>/comment/", views.add_comment, name="add_comment"),
    # Add new comment to a blog post

    path("comment/<int:pk>/delete/", views.delete_comment, name="delete_comment"),
    # Delete comment (author or moderator only)
]
