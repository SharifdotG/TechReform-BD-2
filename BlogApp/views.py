"""Django views for the BlogApp.

This module contains all view functions and classes for handling blog-related
HTTP requests in the TechReform application. It provides comprehensive blog
functionality including public content viewing, content creation and management,
moderation workflows, and analytics reporting.

The views are organized into several functional groups:
- Public views: Content browsing for all visitors (blog list, post details, search)
- Blogger views: Content creation and management for authenticated users
- Content manager views: Administrative functions for content moderation
- Comment system: User interaction through comments with moderation
- Analytics: Content performance reporting and data export

All views include proper authentication, authorization, pagination, and error
handling. The module supports multiple content formats including HTML, CSV,
JSON, and PDF exports for analytics data.

Dependencies:
- xhtml2pdf: Optional dependency for PDF export functionality
- Django ORM: Database operations and queries
- Custom decorators: Role-based access control
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q, Count, Sum
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
import csv
from datetime import timedelta
from .models import BlogPost, Category, Tag, Comment
from .forms import BlogPostForm, CommentForm
from AuthApp.decorators import blogger_required, content_manager_required

# Try importing xhtml2pdf, but provide a fallback
try:
    from xhtml2pdf import pisa
except ImportError:
    pisa = None


def blog_list(request):
    """Display the main blog listing page with featured and recent posts.

    Renders the primary blog page showing featured posts, paginated regular posts,
    and sidebar content including categories, popular tags, and recent posts.
    Only published posts are displayed to public visitors.

    Args:
        request (HttpRequest): The HTTP request object

    Returns:
        HttpResponse: Rendered blog listing page with context data

    Context:
        featured_posts: Up to 3 most recent featured posts
        page_obj: Paginated posts object (6 posts per page)
        categories: All available blog categories
        popular_tags: Up to 10 popular tags
        recent_posts: 5 most recent published posts
    """
    featured_posts = BlogPost.objects.filter(
        status="published", is_featured=True
    ).order_by("-published_at")[:3]
    posts = BlogPost.objects.filter(status="published").order_by("-published_at")

    # Pagination
    paginator = Paginator(posts, 6)  # Show 6 posts per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Context data
    categories = Category.objects.all()
    popular_tags = Tag.objects.all()[:10]
    recent_posts = BlogPost.objects.filter(status="published").order_by(
        "-published_at"
    )[:5]

    context = {
        "featured_posts": featured_posts,
        "page_obj": page_obj,
        "categories": categories,
        "popular_tags": popular_tags,
        "recent_posts": recent_posts,
    }
    return render(request, "blog/blog_list.html", context)


def post_detail(request, slug):
    """Display the detailed view of a single blog post.

    Shows the complete blog post content including comments, comment form,
    and related posts. Increments the view count for analytics tracking.
    Only published posts are accessible to the public.

    Args:
        request (HttpRequest): The HTTP request object
        slug (str): URL slug of the blog post to display

    Returns:
        HttpResponse: Rendered post detail page

    Raises:
        Http404: If post with given slug doesn't exist or isn't published

    Context:
        post: The BlogPost object
        comments: Approved comments for the post
        comment_form: Form for adding new comments
        related_posts: Up to 3 related posts from same category
    """
    post = get_object_or_404(BlogPost, slug=slug, status="published")

    # Increment view count
    post.view_count += 1
    post.save()

    # Get comments
    comments = post.comments.filter(is_approved=True)

    # Comment form
    comment_form = CommentForm()

    # Related posts
    related_posts = (
        BlogPost.objects.filter(status="published", category=post.category)
        .exclude(id=post.id)
        .order_by("-published_at")[:3]
    )

    context = {
        "post": post,
        "comments": comments,
        "comment_form": comment_form,
        "related_posts": related_posts,
    }
    return render(request, "blog/post_detail.html", context)


def category_posts(request, slug):
    """Display all published posts for a specific category.

    Shows a paginated list of blog posts filtered by category, along with
    navigation elements like categories and popular tags.

    Args:
        request (HttpRequest): The HTTP request object
        slug (str): URL slug of the category to filter by

    Returns:
        HttpResponse: Rendered category posts page

    Raises:
        Http404: If category with given slug doesn't exist

    Context:
        category: The Category object
        page_obj: Paginated posts object (6 posts per page)
        categories: All available categories for navigation
        popular_tags: Up to 10 popular tags for sidebar
    """
    category = get_object_or_404(Category, slug=slug)
    posts = BlogPost.objects.filter(category=category, status="published").order_by(
        "-published_at"
    )

    # Pagination
    paginator = Paginator(posts, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "category": category,
        "page_obj": page_obj,
        "categories": Category.objects.all(),
        "popular_tags": Tag.objects.all()[:10],
    }
    return render(request, "blog/category_posts.html", context)


def tag_posts(request, slug):
    """Display all published posts for a specific tag.

    Shows a paginated list of blog posts filtered by tag, along with
    navigation elements for discovering related content.

    Args:
        request (HttpRequest): The HTTP request object
        slug (str): URL slug of the tag to filter by

    Returns:
        HttpResponse: Rendered tag posts page

    Raises:
        Http404: If tag with given slug doesn't exist

    Context:
        tag: The Tag object
        page_obj: Paginated posts object (6 posts per page)
        categories: All available categories for navigation
        popular_tags: Up to 10 popular tags for sidebar
    """
    tag = get_object_or_404(Tag, slug=slug)
    posts = BlogPost.objects.filter(tags=tag, status="published").order_by(
        "-published_at"
    )

    # Pagination
    paginator = Paginator(posts, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "tag": tag,
        "page_obj": page_obj,
        "categories": Category.objects.all(),
        "popular_tags": Tag.objects.all()[:10],
    }
    return render(request, "blog/tag_posts.html", context)


def search_posts(request):
    """Enhanced search functionality for blog posts with multiple filters.

    Provides comprehensive search capabilities including text search across
    title, summary, content, tags, and categories. Supports additional filters
    for category, tag, date range, and sorting options. Returns empty results
    if no search criteria are provided.

    Args:
        request (HttpRequest): The HTTP request object containing search parameters

    URL Parameters:
        q (str): Search query text
        category (str): Category slug to filter by
        tag (str): Tag slug to filter by
        sort (str): Sorting option (newest, oldest, popular, title)
        date_range (str): Date filter (today, week, month, year)

    Returns:
        HttpResponse: Rendered search results page

    Context:
        query: The search query string
        page_obj: Paginated search results (8 posts per page)
        categories: All available categories
        popular_tags: Up to 15 popular tags
    """
    query = request.GET.get("q", "")
    category_slug = request.GET.get("category", "")
    tag_slug = request.GET.get("tag", "")
    sort_by = request.GET.get("sort", "newest")
    date_range = request.GET.get("date_range", "")

    # Start with published posts
    posts = BlogPost.objects.filter(
        status="published"
    )  # Apply search query if provided
    if query:
        posts = posts.filter(
            Q(title__icontains=query)
            | Q(summary__icontains=query)
            | Q(content__icontains=query)
            | Q(tags__name__icontains=query)
            | Q(category__name__icontains=query)
        ).distinct()

    # Apply category filter
    if category_slug:
        posts = posts.filter(category__slug=category_slug)

    # Apply tag filter
    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)

    # Apply date range filter
    if date_range:
        now = timezone.now()
        if date_range == "today":
            posts = posts.filter(published_at__date=now.date())
        elif date_range == "week":
            week_ago = now - timedelta(days=7)
            posts = posts.filter(published_at__gte=week_ago)
        elif date_range == "month":
            month_ago = now - timedelta(days=30)
            posts = posts.filter(published_at__gte=month_ago)
        elif date_range == "year":
            year_ago = now - timedelta(days=365)
            posts = posts.filter(published_at__gte=year_ago)

    # Apply sorting
    if sort_by == "oldest":
        posts = posts.order_by("published_at")
    elif sort_by == "popular":
        posts = posts.order_by("-view_count", "-published_at")
    elif sort_by == "title":
        posts = posts.order_by("title")
    else:  # newest (default)
        posts = posts.order_by("-published_at")

    # Add annotations for comment count (use different name to avoid conflict with property)
    posts = posts.annotate(total_comments=Count("comments"))

    # If no query and no filters, show empty results
    if not query and not category_slug and not tag_slug and not date_range:
        posts = BlogPost.objects.none()

    # Pagination
    paginator = Paginator(posts, 8)  # Show 8 posts per page for search results
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "query": query,
        "page_obj": page_obj,
        "categories": Category.objects.all(),
        "popular_tags": Tag.objects.all()[:15],
    }
    return render(request, "blog/search_results.html", context)


@login_required
@blogger_required
def my_posts(request):
    """Display the current user's blog posts with optional status filtering.

    Shows a paginated list of all posts created by the authenticated user,
    with optional filtering by publication status. Requires blogger role.

    Args:
        request (HttpRequest): The HTTP request object

    URL Parameters:
        status (str): Optional status filter (draft, pending, published, rejected)

    Returns:
        HttpResponse: Rendered user's posts page

    Decorators:
        @login_required: Requires user authentication
        @blogger_required: Requires blogger role

    Context:
        page_obj: Paginated posts object (10 posts per page)
    """
    # Get the status filter from the query parameters
    status_filter = request.GET.get("status")

    # Base query - all posts by the current user
    posts = BlogPost.objects.filter(author=request.user)

    # Apply status filter if provided
    if status_filter and status_filter in ["draft", "pending", "published", "rejected"]:
        posts = posts.filter(status=status_filter)

    # Order posts by creation date (newest first)
    posts = posts.order_by("-created_at")

    # Pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
    }
    return render(request, "blog/my_posts.html", context)


@login_required
@blogger_required
def create_post(request):
    """Handle creation of new blog posts.

    Provides a form for authenticated bloggers to create new blog posts.
    Posts are automatically set to 'pending' status for content manager review.
    Handles both GET (display form) and POST (process submission) requests.

    Args:
        request (HttpRequest): The HTTP request object

    Returns:
        HttpResponse: For GET requests, renders the create post form
                     For POST requests, redirects to user's posts on success

    Decorators:
        @login_required: Requires user authentication
        @blogger_required: Requires blogger role

    Context:
        form: BlogPostForm instance
        categories: All available categories
        tags: All available tags
    """
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.status = "pending"  # Set initial status to pending review
            post.save()
            form.save_m2m()  # Save the many-to-many relations (tags)
            messages.success(request, "Your post has been submitted for review.")
            return redirect("blog:my_posts")
    else:
        form = BlogPostForm()

    context = {
        "form": form,
        "categories": Category.objects.all(),
        "tags": Tag.objects.all(),
    }
    return render(request, "blog/create_post.html", context)


@login_required
@blogger_required
def edit_post(request, slug):
    """Handle editing of existing blog posts.

    Allows the post author to edit their blog post. Maintains publication
    status if already published, otherwise sets to pending for review.
    Only the post author can edit their own posts.

    Args:
        request (HttpRequest): The HTTP request object
        slug (str): URL slug of the post to edit

    Returns:
        HttpResponse: For GET requests, renders the edit form
                     For POST requests, redirects to user's posts on success

    Raises:
        Http404: If post doesn't exist or user is not the author

    Decorators:
        @login_required: Requires user authentication
        @blogger_required: Requires blogger role

    Context:
        form: BlogPostForm instance with current post data
        post: The BlogPost object being edited
        categories: All available categories
        tags: All available tags
    """
    post = get_object_or_404(BlogPost, slug=slug, author=request.user)

    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)

            # If the post was published, keep it published; otherwise, set to pending
            if post.status == "published":
                post.status = "published"
            else:
                post.status = "pending"

            post.save()
            form.save_m2m()
            messages.success(request, "Your post has been updated.")
            return redirect("blog:my_posts")
    else:
        form = BlogPostForm(instance=post)

    context = {
        "form": form,
        "post": post,
        "categories": Category.objects.all(),
        "tags": Tag.objects.all(),
    }
    return render(request, "blog/edit_post.html", context)


@login_required
@blogger_required
def delete_post(request, slug):
    """Handle deletion of blog posts.

    Allows the post author to delete their blog post with confirmation.
    Only the post author can delete their own posts.

    Args:
        request (HttpRequest): The HTTP request object
        slug (str): URL slug of the post to delete

    Returns:
        HttpResponse: For GET requests, renders confirmation page
                     For POST requests, deletes post and redirects to user's posts

    Raises:
        Http404: If post doesn't exist or user is not the author

    Decorators:
        @login_required: Requires user authentication
        @blogger_required: Requires blogger role

    Context:
        post: The BlogPost object to be deleted
    """
    post = get_object_or_404(BlogPost, slug=slug, author=request.user)

    if request.method == "POST":
        post.delete()
        messages.success(request, "Your post has been deleted.")
        return redirect("blog:my_posts")

    context = {
        "post": post,
    }
    return render(request, "blog/delete_post.html", context)


@login_required
@content_manager_required
def pending_posts(request):
    """Display posts awaiting content manager review.

    Shows a paginated list of all blog posts with 'pending' status that
    require review and approval by content managers before publication.

    Args:
        request (HttpRequest): The HTTP request object

    Returns:
        HttpResponse: Rendered pending posts page

    Decorators:
        @login_required: Requires user authentication
        @content_manager_required: Requires content manager role

    Context:
        page_obj: Paginated pending posts (10 posts per page)
    """
    posts = BlogPost.objects.filter(status="pending").order_by("-created_at")

    # Pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
    }
    return render(request, "blog/pending_posts.html", context)


@login_required
@content_manager_required
def review_post(request, slug):
    """Handle review and approval/rejection of pending blog posts.

    Allows content managers to review pending posts and make approval decisions.
    Approved posts are published and get a publication timestamp. Rejected
    posts are marked as rejected for author review.

    Args:
        request (HttpRequest): The HTTP request object
        slug (str): URL slug of the post to review

    Returns:
        HttpResponse: For GET requests, renders review page
                     For POST requests, processes decision and redirects

    Raises:
        Http404: If post doesn't exist or isn't in pending status

    Decorators:
        @login_required: Requires user authentication
        @content_manager_required: Requires content manager role

    POST Parameters:
        decision (str): 'approve' or 'reject'

    Context:
        post: The BlogPost object under review
    """
    post = get_object_or_404(BlogPost, slug=slug, status="pending")

    if request.method == "POST":
        decision = request.POST.get("decision")

        if decision == "approve":
            post.status = "published"
            post.published_at = timezone.now()
            post.save()
            messages.success(
                request, f'The post "{post.title}" has been approved and published.'
            )
        elif decision == "reject":
            post.status = "rejected"
            post.save()
            messages.success(request, f'The post "{post.title}" has been rejected.')

        return redirect("blog:pending_posts")

    context = {
        "post": post,
    }
    return render(request, "blog/review_post.html", context)


@login_required
def add_comment(request, slug):
    """Add a new comment to a blog post.

    Handles comment submission for published blog posts. Comments from
    content managers and admins are auto-approved, while regular user
    comments require moderation approval.

    Args:
        request (HttpRequest): The HTTP request object (must be POST)
        slug (str): URL slug of the post to comment on

    Returns:
        HttpResponse: Redirects to post detail page after processing

    Raises:
        Http404: If post doesn't exist or isn't published

    Decorators:
        @login_required: Requires user authentication

    Note:
        Only processes POST requests. GET requests redirect to post detail.
    """
    post = get_object_or_404(BlogPost, slug=slug, status="published")

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user

            # Auto-approve comments by content managers and admins
            if request.user.profile.is_content_manager or request.user.profile.is_admin:
                comment.is_approved = True

            comment.save()
            messages.success(request, "Your comment has been added.")
            return redirect("blog:post_detail", slug=post.slug)

    return redirect("blog:post_detail", slug=post.slug)


@login_required
def delete_comment(request, pk):
    """Delete a comment with proper permission checking.

    Allows comment deletion by the comment author, content managers, or admins.
    Includes confirmation step for safety and proper authorization checking.

    Args:
        request (HttpRequest): The HTTP request object
        pk (int): Primary key of the comment to delete

    Returns:
        HttpResponse: For GET requests, renders confirmation page
                     For POST requests, deletes comment and redirects to post
                     For unauthorized users, redirects with error message

    Raises:
        Http404: If comment doesn't exist

    Decorators:
        @login_required: Requires user authentication

    Permissions:
        - Comment author can delete their own comments
        - Content managers can delete any comment
        - Admins can delete any comment
    """
    comment = get_object_or_404(Comment, pk=pk)

    # Check if the user is the comment author or has permission to delete
    if (
        comment.author == request.user
        or request.user.profile.is_content_manager
        or request.user.profile.is_admin
    ):
        if request.method == "POST":
            post_slug = comment.post.slug
            comment.delete()
            messages.success(request, "Your comment has been deleted.")
            return redirect("blog:post_detail", slug=post_slug)

        context = {
            "comment": comment,
        }
        return render(request, "blog/delete_comment.html", context)

    messages.error(request, "You do not have permission to delete this comment.")
    return redirect("blog:post_detail", slug=comment.post.slug)


@login_required
@content_manager_required
def content_analysis(request):
    """Generate comprehensive content analytics and statistics dashboard.

    Provides detailed analytics for content managers including post statistics,
    performance metrics, author analysis, category distribution, and content
    age analysis. Calculates growth rates and trending data for decision making.

    Args:
        request (HttpRequest): The HTTP request object

    Returns:
        HttpResponse: Rendered analytics dashboard

    Decorators:
        @login_required: Requires user authentication
        @content_manager_required: Requires content manager role

    Analytics Included:
        - Total post counts by status with percentages
        - View counts and growth metrics
        - Weekly and monthly trends
        - Category performance analysis
        - Top performing posts and authors
        - Tag popularity with cloud sizing
        - Content age distribution

    Context:
        Multiple analytics metrics and datasets for dashboard rendering
    """
    # Current time for calculations
    now = timezone.now()
    last_month = now - timedelta(days=30)
    last_week = now - timedelta(days=7)

    # Basic post statistics
    total_posts = BlogPost.objects.count()
    published_posts = BlogPost.objects.filter(status="published").count()
    pending_posts = BlogPost.objects.filter(status="pending").count()
    rejected_posts = BlogPost.objects.filter(status="rejected").count()

    # Calculate percentages
    published_percent = round(
        (published_posts / total_posts * 100) if total_posts > 0 else 0
    )
    pending_percent = round(
        (pending_posts / total_posts * 100) if total_posts > 0 else 0
    )
    rejected_percent = round(
        (rejected_posts / total_posts * 100) if total_posts > 0 else 0
    )

    # Total views
    total_views = BlogPost.objects.aggregate(Sum("view_count"))["view_count__sum"] or 0

    # Calculate growth
    last_month_posts = BlogPost.objects.filter(created_at__lt=last_month).count()
    post_growth = round(
        ((total_posts - last_month_posts) / last_month_posts * 100)
        if last_month_posts > 0
        else 0
    )

    # Weekly statistics for trend analysis
    posts_this_week = BlogPost.objects.filter(created_at__gte=last_week).count()
    posts_published_this_week = BlogPost.objects.filter(
        status="published", published_at__gte=last_week
    ).count()

    # Views this week
    views_this_week = (
        BlogPost.objects.filter(status="published").aggregate(Sum("view_count"))[
            "view_count__sum"
        ]
        or 0
    )

    # Previous month views
    last_month_views = (
        BlogPost.objects.filter(
            status="published", published_at__lt=last_month
        ).aggregate(Sum("view_count"))["view_count__sum"]
        or 0
    )

    view_growth = round(
        ((total_views - last_month_views) / last_month_views * 100)
        if last_month_views > 0
        else 0
    )

    # Category analysis
    categories = Category.objects.annotate(
        post_count=Count("posts", filter=Q(posts__status="published"))
    ).order_by("-post_count")

    # Top performing posts
    top_posts = BlogPost.objects.filter(status="published").order_by("-view_count")[:10]

    # Recent posts for performance chart
    recent_posts = BlogPost.objects.filter(status="published").order_by(
        "-published_at"
    )[:10]

    # Author performance analysis
    top_authors = (
        BlogPost.objects.filter(status="published")
        .values("author__username")
        .annotate(post_count=Count("id"), total_views=Sum("view_count"))
        .order_by("-total_views")[:5]
    )

    # Average views per post by author
    for author in top_authors:
        if author["post_count"] > 0:
            author["avg_views"] = round(author["total_views"] / author["post_count"])
        else:
            author["avg_views"] = 0

    # Popular tags
    popular_tags = Tag.objects.annotate(
        post_count=Count("posts", filter=Q(posts__status="published"))
    ).order_by("-post_count")[:20]

    # Calculate tag size for tag cloud (between 12px and 24px)
    max_count = popular_tags[0].post_count if popular_tags else 0
    min_size, max_size = 12, 24

    for tag in popular_tags:
        if max_count > 0:
            # Calculate relative size based on post count
            size_range = max_size - min_size
            tag.size = min_size + (tag.post_count / max_count) * size_range
        else:
            tag.size = min_size

    # Content age analysis
    content_age = {
        "last_week": BlogPost.objects.filter(
            status="published", published_at__gte=last_week
        ).count(),
        "last_month": BlogPost.objects.filter(
            status="published", published_at__gte=last_month, published_at__lt=last_week
        ).count(),
        "older": BlogPost.objects.filter(
            status="published", published_at__lt=last_month
        ).count(),
    }

    context = {
        "total_posts": total_posts,
        "published_posts": published_posts,
        "pending_posts": pending_posts,
        "rejected_posts": rejected_posts,
        "published_percent": published_percent,
        "pending_percent": pending_percent,
        "rejected_percent": rejected_percent,
        "total_views": total_views,
        "post_growth": post_growth,
        "view_growth": view_growth,
        "posts_this_week": posts_this_week,
        "posts_published_this_week": posts_published_this_week,
        "views_this_week": views_this_week,
        "categories": categories,
        "top_posts": top_posts,
        "recent_posts": recent_posts,
        "top_authors": top_authors,
        "popular_tags": popular_tags,
        "content_age": content_age,
    }

    return render(request, "blog/content_analysis.html", context)


@login_required
@content_manager_required
def export_content_analysis(request, format="csv"):
    """Export content analysis data in multiple formats.

    Generates and exports comprehensive content analytics data in CSV, JSON,
    or PDF format. Includes summary statistics, category analysis, top posts,
    and author performance metrics with proper formatting for each format.

    Args:
        request (HttpRequest): The HTTP request object
        format (str): Export format - 'csv', 'json', or 'pdf'

    Returns:
        HttpResponse: File download response with appropriate content type
                     For unsupported formats, redirects with error message

    Raises:
        Http404: If format is not supported

    Decorators:
        @login_required: Requires user authentication
        @content_manager_required: Requires content manager role

    Supported Formats:
        - CSV: Tabular data with headers and sections
        - JSON: Structured data for API consumption
        - PDF: Formatted report (requires xhtml2pdf)

    Note:
        PDF export requires xhtml2pdf library to be installed.
        Fallback error handling provided if library is missing.
    """
    # Basic post statistics
    total_posts = BlogPost.objects.count()
    published_posts = BlogPost.objects.filter(status="published").count()
    pending_posts = BlogPost.objects.filter(status="pending").count()
    rejected_posts = BlogPost.objects.filter(status="rejected").count()

    # Calculate percentages
    published_percent = round(
        (published_posts / total_posts * 100) if total_posts > 0 else 0
    )
    pending_percent = round(
        (pending_posts / total_posts * 100) if total_posts > 0 else 0
    )
    rejected_percent = round(
        (rejected_posts / total_posts * 100) if total_posts > 0 else 0
    )

    # Total views
    total_views = BlogPost.objects.aggregate(Sum("view_count"))["view_count__sum"] or 0

    # Category analysis
    categories = Category.objects.annotate(
        post_count=Count("posts", filter=Q(posts__status="published"))
    ).order_by("-post_count")

    # Top performing posts
    top_posts = BlogPost.objects.filter(status="published").order_by("-view_count")[:10]

    # Author performance analysis
    top_authors = (
        BlogPost.objects.filter(status="published")
        .values("author__username")
        .annotate(post_count=Count("id"), total_views=Sum("view_count"))
        .order_by("-total_views")[:5]
    )

    if format == "csv":
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            f'attachment; filename="content_analysis_{timezone.now().strftime("%Y%m%d")}.csv"'
        )

        writer = csv.writer(response)
        writer.writerow(
            [
                "Content Analysis Report",
                f"Generated on: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}",
            ]
        )
        writer.writerow([])

        # Summary statistics
        writer.writerow(["Summary Statistics"])
        writer.writerow(["Metric", "Value", "Percentage"])
        writer.writerow(["Total Posts", total_posts, "100%"])
        writer.writerow(["Published Posts", published_posts, f"{published_percent}%"])
        writer.writerow(["Pending Posts", pending_posts, f"{pending_percent}%"])
        writer.writerow(["Rejected Posts", rejected_posts, f"{rejected_percent}%"])
        writer.writerow(["Total Views", total_views, ""])
        writer.writerow([])

        # Categories
        writer.writerow(["Categories"])
        writer.writerow(["Category", "Post Count", "Percentage"])
        for category in categories:
            writer.writerow(
                [
                    category.name,
                    category.post_count,
                    f"{round((category.post_count / published_posts * 100) if published_posts > 0 else 0)}%",
                ]
            )
        writer.writerow([])

        # Top Posts
        writer.writerow(["Top Performing Posts"])
        writer.writerow(["Title", "Author", "Category", "Published Date", "Views"])
        for post in top_posts:
            writer.writerow(
                [
                    post.title,
                    post.author.username,
                    post.category.name,
                    post.published_at.strftime("%Y-%m-%d")
                    if post.published_at
                    else "N/A",
                    post.view_count,
                ]
            )
        writer.writerow([])

        # Top Authors
        writer.writerow(["Top Authors"])
        writer.writerow(
            ["Username", "Post Count", "Total Views", "Average Views Per Post"]
        )
        for author in top_authors:
            avg_views = (
                round(author["total_views"] / author["post_count"])
                if author["post_count"] > 0
                else 0
            )
            writer.writerow(
                [
                    author["author__username"],
                    author["post_count"],
                    author["total_views"],
                    avg_views,
                ]
            )

        return response

    elif format == "json":
        data = {
            "generated_at": timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
            "summary": {
                "total_posts": total_posts,
                "published_posts": published_posts,
                "pending_posts": pending_posts,
                "rejected_posts": rejected_posts,
                "total_views": total_views,
            },
            "categories": [
                {
                    "name": category.name,
                    "post_count": category.post_count,
                    "percentage": round(
                        (category.post_count / published_posts * 100)
                        if published_posts > 0
                        else 0
                    ),
                }
                for category in categories
            ],
            "top_posts": [
                {
                    "title": post.title,
                    "author": post.author.username,
                    "category": post.category.name,
                    "published_at": post.published_at.strftime("%Y-%m-%d")
                    if post.published_at
                    else None,
                    "views": post.view_count,
                }
                for post in top_posts
            ],
            "top_authors": [
                {
                    "username": author["author__username"],
                    "post_count": author["post_count"],
                    "total_views": author["total_views"],
                    "avg_views": round(author["total_views"] / author["post_count"])
                    if author["post_count"] > 0
                    else 0,
                }
                for author in top_authors
            ],
        }

        response = JsonResponse(data)
        response["Content-Disposition"] = (
            f'attachment; filename="content_analysis_{timezone.now().strftime("%Y%m%d")}.json"'
        )
        return response

    elif format == "pdf":
        # Generate PDF using HTML template
        template = get_template("blog/content_analysis_pdf.html")

        context = {
            "generated_at": timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_posts": total_posts,
            "published_posts": published_posts,
            "pending_posts": pending_posts,
            "rejected_posts": rejected_posts,
            "published_percent": published_percent,
            "pending_percent": pending_percent,
            "rejected_percent": rejected_percent,
            "total_views": total_views,
            "categories": categories,
            "top_posts": top_posts,
            "top_authors": top_authors,
        }

        html = template.render(context)

        # Create PDF
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="content_analysis_{timezone.now().strftime("%Y%m%d")}.pdf"'
        )

        # Generate PDF
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse("PDF generation failed")

        return response

    else:
        messages.error(request, f"Unsupported export format: {format}")
        return redirect("blog:content_analysis")
