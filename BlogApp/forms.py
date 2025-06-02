"""Django forms for the BlogApp.

This module contains Django form classes for handling blog-related data input
and validation. It provides user-friendly forms for creating and editing blog
content including posts, comments, categories, and tags.

The forms include:
- BlogPostForm: Comprehensive form for creating and editing blog posts
- CommentForm: Simple form for user comments on blog posts
- CategoryForm: Form for managing blog categories
- TagForm: Form for creating and managing blog tags

All forms are styled with Tailwind CSS classes for consistent UI appearance
and include appropriate validation and widget configurations.
"""

from django import forms
from .models import BlogPost, Comment, Category, Tag
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class BlogPostForm(forms.ModelForm):
    """Django form for creating and editing blog posts.

    This form provides a comprehensive interface for blog post creation and
    editing with rich text editing capabilities, category selection, tag
    assignment, and image upload functionality.

    Features:
    - Rich text editor (CKEditor) for content with file upload support
    - Category selection with dropdown
    - Multiple tag selection
    - Featured image upload
    - Summary text area
    - Tailwind CSS styling for consistent UI

    Fields:
        title: Post title with styled text input
        category: Dropdown selection from available categories
        tags: Multiple selection widget for tag assignment (optional)
        featured_image: File input for post featured image
        summary: Textarea for post summary/excerpt
        content: Rich text editor with upload capabilities
    """

    content = forms.CharField(widget=CKEditorUploadingWidget())
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select Category",
        widget=forms.Select(attrs={"class": "select select-bordered w-full"}),
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "select select-bordered w-full"}),
        required=False,
    )

    class Meta:
        model = BlogPost
        fields = ["title", "category", "tags", "featured_image", "summary", "content"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Enter post title",
                }
            ),
            "summary": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full",
                    "rows": 3,
                    "placeholder": "Brief summary of your post",
                }
            ),
            "featured_image": forms.FileInput(
                attrs={"class": "file-input file-input-bordered w-full"}
            ),
        }


class CommentForm(forms.ModelForm):
    """Django form for user comments on blog posts.

    A simple, user-friendly form that allows visitors to leave comments
    on blog posts. The form includes validation and styling for a clean
    user experience.

    Features:
    - Textarea for comment content
    - Tailwind CSS styling for consistent appearance
    - Placeholder text for user guidance
    - Responsive design

    Fields:
        content: Textarea for the comment text with 4 rows height
    """

    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full",
                    "rows": 4,
                    "placeholder": "Write your comment here...",
                }
            ),
        }


class CategoryForm(forms.ModelForm):
    """Django form for creating and managing blog categories.

    This form allows administrators and authorized users to create and
    edit blog categories. Categories help organize blog posts into
    logical groups for better navigation and content discovery.

    Features:
    - Category name input with validation
    - Optional description field
    - Tailwind CSS styling for admin interface consistency
    - User-friendly placeholders

    Fields:
        name: Text input for the category name
        description: Optional textarea for category description
    """

    class Meta:
        model = Category
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Category name",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full",
                    "rows": 3,
                    "placeholder": "Category description (optional)",
                }
            ),
        }


class TagForm(forms.ModelForm):
    """Django form for creating and managing blog tags.

    A simple form for creating blog tags that can be associated with
    blog posts. Tags provide a flexible way to label and categorize
    content for improved searchability and content discovery.

    Features:
    - Simple text input for tag name
    - Tailwind CSS styling for consistency
    - User-friendly placeholder text
    - Validation for tag name uniqueness

    Fields:
        name: Text input for the tag name
    """

    class Meta:
        model = Tag
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Tag name",
                }
            ),
        }
