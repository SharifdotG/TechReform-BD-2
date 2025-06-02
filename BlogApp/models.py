"""Django models for the BlogApp.

This module defines the database models for the blog functionality of the
TechReform application. It includes models for blog posts, categories, tags,
and comments, providing a complete blogging system with content management
and user interaction capabilities.

The models include:
- Category: Organizational structure for grouping blog posts
- Tag: Flexible labeling system for content categorization
- BlogPost: Main content model with rich text, images, and metadata
- Comment: User interaction model for blog post discussions

All models include automatic slug generation, timestamp tracking, and
appropriate relationships for a fully functional blog system.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    """Model representing blog post categories.

    Categories provide a hierarchical organization system for blog posts,
    allowing content to be grouped into logical sections for better
    navigation and content discovery.

    Attributes:
        name (CharField): The display name of the category (max 100 chars)
        slug (SlugField): URL-friendly identifier, auto-generated from name
        description (TextField): Optional detailed description of the category
        created_at (DateTimeField): Timestamp when category was created
        updated_at (DateTimeField): Timestamp when category was last modified

    Meta:
        verbose_name_plural: 'Categories'
        ordering: Alphabetical by name

    Methods:
        __str__: Returns the category name
        save: Auto-generates slug from name if not provided
        get_absolute_url: Returns URL for viewing posts in this category
    """

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Save the category instance with auto-generated slug.

        Automatically generates a URL-friendly slug from the category name
        if no slug is provided. This ensures all categories have valid
        URLs for web access.

        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Get the absolute URL for this category.

        Returns the URL where visitors can view all blog posts
        belonging to this category.

        Returns:
            str: The absolute URL path for the category page
        """
        return reverse("blog:category_posts", args=[self.slug])


class Tag(models.Model):
    """Model representing blog post tags.

    Tags provide a flexible labeling system for blog posts, allowing
    content to be categorized with multiple keywords for improved
    searchability and content discovery.

    Attributes:
        name (CharField): The display name of the tag (max 50 chars)
        slug (SlugField): URL-friendly identifier, auto-generated from name

    Meta:
        ordering: Alphabetical by name

    Methods:
        __str__: Returns the tag name
        save: Auto-generates slug from name if not provided
        get_absolute_url: Returns URL for viewing posts with this tag
    """

    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Save the tag instance with auto-generated slug.

        Automatically generates a URL-friendly slug from the tag name
        if no slug is provided. This ensures all tags have valid
        URLs for web access.

        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Get the absolute URL for this tag.

        Returns the URL where visitors can view all blog posts
        tagged with this tag.

        Returns:
            str: The absolute URL path for the tag page
        """
        return reverse("blog:tag_posts", args=[self.slug])


class BlogPost(models.Model):
    """Model representing a blog post.

    The main content model for the blog system, supporting rich text content,
    featured images, categorization, tagging, and publication workflow.
    Includes view tracking and comprehensive metadata.

    Attributes:
        STATUS_CHOICES (tuple): Available publication status options
        title (CharField): The post title (max 200 chars)
        slug (SlugField): URL-friendly identifier, auto-generated from title
        author (ForeignKey): Reference to the User who created the post
        category (ForeignKey): Reference to the post's Category
        tags (ManyToManyField): Associated Tag objects for the post
        featured_image (ImageField): Optional featured image with date-based upload path
        summary (TextField): Brief description/excerpt (max 500 chars)
        content (RichTextUploadingField): Main post content with rich text editing
        status (CharField): Publication status (draft, pending, published, rejected)
        is_featured (BooleanField): Whether this post should be highlighted
        view_count (PositiveIntegerField): Number of times the post has been viewed
        created_at (DateTimeField): Timestamp when post was created
        updated_at (DateTimeField): Timestamp when post was last modified
        published_at (DateTimeField): Timestamp when post was published

    Meta:
        ordering: Newest posts first
        indexes: Optimized for slug and creation date queries

    Methods:
        __str__: Returns the post title
        save: Auto-generates slug from title if not provided
        get_absolute_url: Returns URL for viewing this post
        comment_count: Property returning count of approved comments
    """

    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("pending", "Pending Review"),
        ("published", "Published"),
        ("rejected", "Rejected"),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="posts"
    )
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)
    featured_image = models.ImageField(
        upload_to="blog/images/%Y/%m/%d/", blank=True, null=True
    )
    summary = models.TextField(max_length=500)
    content = RichTextUploadingField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    is_featured = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Save the blog post instance with auto-generated slug.

        Automatically generates a URL-friendly slug from the post title
        if no slug is provided. This ensures all posts have valid
        URLs for web access.

        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Get the absolute URL for this blog post.

        Returns the URL where visitors can view the full blog post
        content and interact with comments.

        Returns:
            str: The absolute URL path for the blog post detail page
        """
        return reverse("blog:post_detail", args=[self.slug])

    @property
    def comment_count(self):
        """Get the count of approved comments for this post.

        Returns the number of comments that have been approved by
        moderators and are visible to site visitors.

        Returns:
            int: The number of approved comments on this post
        """
        return self.comments.filter(is_approved=True).count()


class Comment(models.Model):
    """Model representing comments on blog posts.

    Enables user interaction with blog content through a commenting system
    with moderation capabilities. Comments require approval before being
    displayed to ensure content quality.

    Attributes:
        post (ForeignKey): Reference to the BlogPost being commented on
        author (ForeignKey): Reference to the User who wrote the comment
        content (TextField): The text content of the comment
        is_approved (BooleanField): Whether the comment has been approved for display
        created_at (DateTimeField): Timestamp when comment was created
        updated_at (DateTimeField): Timestamp when comment was last modified

    Meta:
        ordering: Newest comments first

    Methods:
        __str__: Returns a descriptive string with author and post information
    """

    post = models.ForeignKey(
        BlogPost, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
