"""
Django models for user authentication, profiles, and customer support.

This module contains the core models for the AuthApp, including user profile
management with role-based access control and a comprehensive customer support
ticket system. The models provide functionality for user authentication,
profile customization, and customer service management.

Models included:
    - UserProfile: Extended user information with role-based permissions
    - SupportCategory: Categories for organizing support tickets
    - SupportTicket: Customer support ticket management system
    - SupportResponse: Messages and responses within support tickets

The module also includes Django signals for automatic profile creation and
default category setup, ensuring proper initialization of user accounts and
support system components.
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class UserProfile(models.Model):
    """
    Extended user profile model with role-based access control.

    This model extends Django's built-in User model to provide additional
    profile information and implements a comprehensive role-based permission
    system. It automatically creates profiles for new users and manages
    user roles, verification status, and profile customization.

    Attributes:
        ROLE_CHOICES (tuple): Available user roles in the system
        user (OneToOneField): Link to Django User model
        role (CharField): User's role for permission control
        phone (CharField): User's phone number (optional)
        address (TextField): User's address (optional)
        profile_image (ImageField): User's profile picture (optional)
        is_verified (BooleanField): User verification status
        created_at (DateTimeField): Profile creation timestamp
        updated_at (DateTimeField): Last profile update timestamp

    Methods:
        full_name: Property returning user's full name
        is_admin: Check if user has admin privileges
        is_staff: Check if user has staff privileges
        is_content_manager: Check if user can manage content
        is_blogger: Check if user can create blog posts
        is_regular_user: Check if user has basic user privileges
        is_guest: Check if user is a guest

    Example:
        profile = user.profile
        if profile.is_admin():
            # Admin-only functionality
            pass
    """

    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("staff", "Staff"),
        ("content_manager", "Content Manager"),
        ("user", "User"),
        ("blogger", "Blogger"),
        ("guest", "Guest"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(
        upload_to="profile_images/", blank=True, null=True
    )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return string representation of the user profile."""
        return f"{self.user.username} - {self.get_role_display()}"

    @property
    def full_name(self):
        """
        Get the user's full name from first and last name.

        Returns:
            str: Full name if both first and last names exist, empty string otherwise
        """
        if not self.user.first_name and not self.user.last_name:
            return ""
        return f"{self.user.first_name} {self.user.last_name}"

    def is_admin(self):
        """
        Check if user has admin role.

        Returns:
            bool: True if user is an admin, False otherwise
        """
        return self.role == "admin"

    def is_staff(self):
        """
        Check if user has staff or admin privileges.

        Returns:
            bool: True if user is staff or admin, False otherwise
        """
        return self.role == "staff" or self.role == "admin"

    def is_content_manager(self):
        """
        Check if user can manage content.

        Returns:
            bool: True if user is content manager or admin, False otherwise
        """
        return self.role == "content_manager" or self.role == "admin"

    def is_blogger(self):
        """
        Check if user can create and manage blog posts.

        Returns:
            bool: True if user is blogger or admin, False otherwise
        """
        return self.role == "blogger" or self.role == "admin"

    def is_regular_user(self):
        """
        Check if user has regular user privileges or higher.

        Returns:
            bool: True if user has any recognized role except guest, False otherwise
        """
        return self.role == "user" or self.role in [
            "admin",
            "staff",
            "content_manager",
            "blogger",
        ]

    def is_guest(self):
        """
        Check if user is a guest with limited privileges.

        Returns:
            bool: True if user is a guest, False otherwise
        """
        return self.role == "guest"


# Signal to create or update user profile when user is created or updated
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Django signal to automatically create or update user profiles.

    This signal handler ensures that every User instance has an associated
    UserProfile. It automatically creates profiles for new users and maintains
    proper role assignments, especially for superusers.

    Args:
        sender (Model): The User model class
        instance (User): The specific User instance being saved
        created (bool): True if this is a new user, False if updating existing
        **kwargs: Additional keyword arguments from the signal

    Behavior:
        - New users: Creates UserProfile with 'admin' role for superusers, 'user' for others
        - Existing users: Ensures superusers have 'admin' role, saves profile if exists

    Note:
        This signal automatically fires whenever a User instance is saved,
        ensuring data consistency between User and UserProfile models.
    """
    if created:
        # Ensure the role is set to 'admin' for superusers
        role = "admin" if instance.is_superuser else "user"
        UserProfile.objects.create(user=instance, role=role)
    else:
        # Ensure superusers always have admin role
        if (
            instance.is_superuser
            and hasattr(instance, "profile")
            and instance.profile.role != "admin"
        ):
            instance.profile.role = "admin"

        # Update the profile if it exists
        if hasattr(instance, "profile"):
            instance.profile.save()


class SupportCategory(models.Model):
    """
    Categories for organizing customer support tickets.

    This model defines categories that can be assigned to support tickets
    to help organize and route customer inquiries appropriately. Categories
    can be customized with colors for visual organization and can be
    activated/deactivated as needed.

    Attributes:
        name (CharField): Unique category name (max 100 chars)
        description (TextField): Optional detailed description of the category
        color (CharField): Hex color code for visual identification (default: #007bff)
        is_active (BooleanField): Whether category is currently available for use
        created_at (DateTimeField): Timestamp when category was created

    Methods:
        __str__: Returns the category name

    Meta:
        verbose_name_plural: "Support Categories"
        ordering: Alphabetical by name

    Example:
        category = SupportCategory.objects.create(
            name="Technical Support",
            description="Hardware and software issues",
            color="#dc3545"
        )
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(
        max_length=7, default="#007bff", help_text="Hex color code for category"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Support Categories"
        ordering = ["name"]

    def __str__(self):
        """Return the category name."""
        return self.name


class SupportTicket(models.Model):
    """
    Comprehensive customer support ticket management system.

    This model handles all aspects of customer support tickets including
    ticket creation, assignment, status tracking, priority management,
    and resolution. It provides a complete ticketing system with automatic
    ID generation, time tracking, and overdue detection.

    Attributes:
        STATUS_CHOICES (list): Available ticket status options
        PRIORITY_CHOICES (list): Available priority levels
        ticket_id (CharField): Unique ticket identifier (auto-generated)
        customer (ForeignKey): User who created the ticket
        subject (CharField): Brief description of the issue
        category (ForeignKey): Optional category for organization
        description (TextField): Detailed issue description
        customer_email (EmailField): Contact email address
        customer_phone (CharField): Optional contact phone number
        status (CharField): Current ticket status
        priority (CharField): Ticket priority level
        assigned_staff (ForeignKey): Staff member assigned to ticket
        order_number (CharField): Related order if applicable
        product_info (TextField): Product details if relevant
        attachment (FileField): Optional file attachment
        created_at (DateTimeField): Ticket creation timestamp
        updated_at (DateTimeField): Last modification timestamp
        resolved_at (DateTimeField): Resolution timestamp
        closed_at (DateTimeField): Closure timestamp
        internal_notes (TextField): Staff-only internal notes

    Properties:
        is_overdue: Checks if ticket exceeds priority-based time thresholds
        time_since_creation: Human-readable time since creation

    Methods:
        save: Custom save with auto ID generation and timestamp management
        __str__: Returns ticket ID and subject

    Meta:
        ordering: Most recent first
        indexes: Optimized for common query patterns

    Example:
        ticket = SupportTicket.objects.create(
            customer=user,
            subject="Login Issues",
            description="Cannot access my account",
            customer_email=user.email,
            priority="high"
        )
    """

    STATUS_CHOICES = [
        ("open", "Open"),
        ("in_progress", "In Progress"),
        ("pending_customer", "Pending Customer Response"),
        ("resolved", "Resolved"),
        ("closed", "Closed"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("urgent", "Urgent"),
    ]

    # Basic Information
    ticket_id = models.CharField(max_length=20, unique=True, editable=False)
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="support_tickets"
    )
    subject = models.CharField(max_length=200)
    category = models.ForeignKey(
        SupportCategory, on_delete=models.SET_NULL, null=True, blank=True
    )
    description = models.TextField()

    # Contact Information
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20, blank=True)

    # Ticket Management
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default="medium"
    )
    assigned_staff = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tickets",
        limit_choices_to={"profile__role__in": ["staff", "admin"]},
    )

    # Additional Information
    order_number = models.CharField(
        max_length=50, blank=True, help_text="Related order number if applicable"
    )
    product_info = models.TextField(
        blank=True, help_text="Product details if issue is product-related"
    )
    attachment = models.FileField(
        upload_to="support_attachments/", blank=True, null=True
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    # Staff Notes (Internal)
    internal_notes = models.TextField(
        blank=True, help_text="Internal notes for staff only"
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "priority"]),
            models.Index(fields=["customer", "status"]),
            models.Index(fields=["assigned_staff", "status"]),
        ]

    def __str__(self):
        """Return string representation of the ticket."""
        return f"#{self.ticket_id} - {self.subject}"

    def save(self, *args, **kwargs):
        """
        Custom save method with automatic ID generation and timestamp management.

        This method handles:
        - Automatic ticket ID generation using UUID if not already set
        - Automatic timestamp setting for resolved_at when status changes to 'resolved'
        - Automatic timestamp setting for closed_at when status changes to 'closed'

        Args:
            *args: Variable length argument list passed to parent save()
            **kwargs: Arbitrary keyword arguments passed to parent save()

        Note:
            Ticket IDs are generated in format "TR{8-char-UUID}" for uniqueness
            Timestamps are only set once when status first changes to resolved/closed
        """
        if not self.ticket_id:
            # Generate unique ticket ID
            import uuid

            self.ticket_id = f"TR{str(uuid.uuid4())[:8].upper()}"

        # Auto-set timestamps based on status changes
        if self.status == "resolved" and not self.resolved_at:
            self.resolved_at = timezone.now()
        elif self.status == "closed" and not self.closed_at:
            self.closed_at = timezone.now()

        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        """
        Check if ticket is overdue based on priority and creation time.

        Determines if a ticket has exceeded the expected response time based
        on its priority level. Resolved and closed tickets are never overdue.

        Priority Thresholds:
            - Urgent: 2 hours
            - High: 8 hours
            - Medium: 24 hours (1 day)
            - Low: 72 hours (3 days)

        Returns:
            bool: True if ticket is overdue, False otherwise

        Note:
            Tickets with 'resolved' or 'closed' status always return False
        """
        if self.status in ["resolved", "closed"]:
            return False

        hours_since_creation = (timezone.now() - self.created_at).total_seconds() / 3600
        priority_thresholds = {
            "urgent": 2,  # 2 hours
            "high": 8,  # 8 hours
            "medium": 24,  # 1 day
            "low": 72,  # 3 days
        }
        return hours_since_creation > priority_thresholds.get(self.priority, 24)

    @property
    def time_since_creation(self):
        """
        Get human-readable time since ticket creation.

        Provides a user-friendly representation of how long ago the ticket
        was created, automatically choosing appropriate time units.

        Returns:
            str: Human-readable time difference (e.g., "2 days ago", "3 hours ago")

        Time Units:
            - Days: For differences >= 1 day
            - Hours: For differences >= 1 hour but < 1 day
            - Minutes: For differences >= 1 minute but < 1 hour
            - "Just now": For differences < 1 minute
        """
        delta = timezone.now() - self.created_at
        if delta.days > 0:
            return f"{delta.days} day{'s' if delta.days != 1 else ''} ago"
        elif delta.seconds > 3600:
            hours = delta.seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif delta.seconds > 60:
            minutes = delta.seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        else:
            return "Just now"


class SupportResponse(models.Model):
    """
    Messages and responses within support tickets.

    This model handles all communication within a support ticket, including
    customer messages, staff responses, and internal notes. It automatically
    detects staff responses and supports file attachments for comprehensive
    customer support communication.

    Attributes:
        ticket (ForeignKey): The support ticket this response belongs to
        author (ForeignKey): User who created the response
        message (TextField): The response message content
        attachment (FileField): Optional file attachment
        is_internal (BooleanField): Whether response is internal staff note
        is_staff_response (BooleanField): Auto-detected staff response flag
        created_at (DateTimeField): Response creation timestamp

    Methods:
        save: Custom save with automatic staff response detection
        __str__: Returns response description with author and ticket

    Meta:
        ordering: Chronological order (oldest first)

    Example:
        response = SupportResponse.objects.create(
            ticket=ticket,
            author=staff_user,
            message="We're looking into this issue.",
            is_internal=False
        )
    """

    ticket = models.ForeignKey(
        SupportTicket, on_delete=models.CASCADE, related_name="responses"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    attachment = models.FileField(upload_to="support_responses/", blank=True, null=True)
    is_internal = models.BooleanField(
        default=False, help_text="Internal note visible only to staff"
    )
    is_staff_response = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        """Return response description with author and ticket."""
        return f"Response by {self.author.username} on {self.ticket.ticket_id}"

    def save(self, *args, **kwargs):
        """
        Custom save method with automatic staff response detection.

        This method automatically sets the is_staff_response flag based on
        the author's profile role. Users with staff privileges have their
        responses automatically marked as staff responses.

        Args:
            *args: Variable length argument list passed to parent save()
            **kwargs: Arbitrary keyword arguments passed to parent save()

        Note:
            Staff detection is based on the author's UserProfile.is_staff() method
        """
        # Auto-detect if this is a staff response
        if hasattr(self.author, "profile") and self.author.profile.is_staff():
            self.is_staff_response = True
        super().save(*args, **kwargs)


# Signal to create default support categories
@receiver(post_save, sender=User)
def create_default_support_categories(sender, created, **kwargs):
    """
    Django signal to create default support categories on first user creation.

    This signal handler ensures that the support system has default categories
    available when the first user is created. It only runs once and creates
    a comprehensive set of common support categories with appropriate colors
    and descriptions.

    Args:
        sender (Model): The User model class
        created (bool): True if this is a new user, False if updating existing
        **kwargs: Additional keyword arguments from the signal

    Default Categories Created:
        - Technical Support (red): Hardware/software issues
        - Order Issues (orange): Order, shipping, payment problems
        - Product Inquiry (blue): Product questions and compatibility
        - Account Issues (purple): User account and login problems
        - Billing Support (green): Payment, refund, billing questions
        - General Inquiry (gray): General questions and feedback

    Note:
        This signal only executes when no SupportCategory objects exist,
        ensuring categories are created only once during system initialization.
    """
    if created and not SupportCategory.objects.exists():
        default_categories = [
            {
                "name": "Technical Support",
                "description": "Technical issues with products or website",
                "color": "#dc3545",
            },
            {
                "name": "Order Issues",
                "description": "Problems with orders, shipping, or payments",
                "color": "#fd7e14",
            },
            {
                "name": "Product Inquiry",
                "description": "Questions about products, compatibility, or specifications",
                "color": "#0d6efd",
            },
            {
                "name": "Account Issues",
                "description": "Problems with user accounts or login",
                "color": "#6f42c1",
            },
            {
                "name": "Billing Support",
                "description": "Payment, refund, or billing related questions",
                "color": "#198754",
            },
            {
                "name": "General Inquiry",
                "description": "General questions or feedback",
                "color": "#6c757d",
            },
        ]

        for category_data in default_categories:
            SupportCategory.objects.create(**category_data)
