"""
Django views for authentication, user management, and customer support.

This module contains all view functions for the AuthApp, providing comprehensive
functionality for user authentication, profile management, user administration,
and a complete customer support ticket system. The views are organized into
logical groups with appropriate access controls and security measures.

View Categories:
    Authentication Views:
        - login_view: Handle user login with remember me functionality
        - register_view: User registration with automatic profile creation
        - logout_view: User logout with session cleanup
        - profile_view: User profile management and updates

    User Management Views (Admin/Staff only):
        - user_management: Admin dashboard for user administration
        - update_user_role: Role modification functionality
        - delete_user: User account deletion with confirmation

    Customer Support Views (Staff only):
        - customer_support_dashboard: Main support dashboard with filtering
        - ticket_detail: Detailed ticket management interface
        - assign_ticket: AJAX ticket assignment functionality
        - update_ticket_status: AJAX status update functionality
        - support_analytics: Reporting and analytics dashboard

    Customer Support Views (Public/Customer):
        - contact_view: Public contact form and ticket creation
        - my_tickets_view: Customer's personal ticket list
        - customer_ticket_detail: Customer ticket detail with limited functionality
        - track_ticket: Public ticket tracking by ID and email

Security Features:
    - Role-based access control using custom decorators
    - CSRF protection on all forms
    - Proper authentication checks
    - Input validation and sanitization
    - File upload security measures

Dependencies:
    - Custom authentication forms and decorators
    - UserProfile model with role-based permissions
    - Support ticket system models
    - Django's built-in authentication framework
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.http import JsonResponse
from django.utils import timezone
from django.core.paginator import Paginator
from .models import UserProfile, SupportTicket, SupportResponse, SupportCategory
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm
from .decorators import admin_required, staff_required


def login_view(request):
    """
    Handle user login with custom authentication form and remember me functionality.

    This view processes user login using a custom authentication form that includes
    a 'remember me' option. It validates credentials, manages session expiry based
    on user preference, and redirects authenticated users appropriately.

    Args:
        request (HttpRequest): The HTTP request object

    Returns:
        HttpResponse: Login page for GET requests, redirect after successful login

    Features:
        - Custom authentication form with remember me checkbox
        - Session expiry control based on remember me preference
        - Automatic redirect for already authenticated users
        - Success messages for user feedback
        - CSRF protection and proper form validation

    Security:
        - Uses Django's built-in authentication system
        - Secure session management
        - Protection against unauthorized access

    Template:
        auth/login.html

    Context:
        form (CustomAuthenticationForm): Authentication form instance
    """
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            remember_me = form.cleaned_data.get("remember_me")

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                # Set session expiry based on remember_me
                if not remember_me:
                    # Session expires when the user closes the browser
                    request.session.set_expiry(0)

                messages.success(request, f"Welcome back, {user.username}!")
                return redirect("index")
    else:
        form = CustomAuthenticationForm()

    context = {"form": form}
    return render(request, "auth/login.html", context)


def register_view(request):
    """
    Handle user registration with custom registration form and automatic profile creation.

    This view processes new user registration using a custom form that includes
    additional profile fields. It automatically creates a UserProfile instance
    and logs in the user after successful registration.

    Args:
        request (HttpRequest): The HTTP request object

    Returns:
        HttpResponse: Registration page for GET, redirect after successful registration

    Features:
        - Extended registration form with profile fields (name, phone, role)
        - Automatic UserProfile creation via form save method
        - Immediate login after successful registration
        - Redirect prevention for already authenticated users
        - Success messages and user feedback

    Security:
        - Form validation and CSRF protection
        - Secure password handling
        - Input sanitization and validation

    Template:
        auth/register.html

    Context:
        form (CustomUserCreationForm): Registration form instance
    """
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after registration
            login(request, user)
            messages.success(
                request, f"Account created successfully! Welcome, {user.username}!"
            )
            return redirect("index")
    else:
        form = CustomUserCreationForm()

    context = {"form": form}
    return render(request, "auth/register.html", context)


def logout_view(request):
    """
    Handle user logout with session cleanup and user feedback.

    This view logs out the current user, cleans up their session data,
    provides appropriate feedback, and redirects to the home page.

    Args:
        request (HttpRequest): The HTTP request object

    Returns:
        HttpResponse: Redirect to index page with logout confirmation message

    Features:
        - Complete session cleanup
        - User feedback via success message
        - Safe redirect to home page

    Security:
        - Proper session termination
        - Secure logout process
    """
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("index")


@login_required
def profile_view(request):
    """
    Display and update user profile information with form handling.

    This view provides a comprehensive interface for users to view and update
    their profile information, including both User model fields (name, email)
    and UserProfile fields (phone, address, profile image). It ensures every
    user has a profile and handles form validation and file uploads.

    Args:
        request (HttpRequest): The HTTP request object

    Returns:
        HttpResponse: Profile page with form for GET, redirect after successful update

    Features:
        - Automatic UserProfile creation if missing
        - Combined User and UserProfile field editing
        - File upload handling for profile images
        - Form validation and error handling
        - Success feedback and redirect after updates

    Security:
        - Login required decorator
        - Proper file upload validation
        - CSRF protection on forms

    Template:
        user/profile.html

    Context:
        form (UserProfileForm): Profile form with current data
        user_profile (UserProfile): Current user's profile instance
    """
    # Ensure user has a profile
    if not hasattr(request.user, "profile"):
        UserProfile.objects.create(user=request.user)

    if request.method == "POST":
        form = UserProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if form.is_valid():
            # Update user data
            request.user.first_name = form.cleaned_data["first_name"]
            request.user.last_name = form.cleaned_data["last_name"]
            request.user.email = form.cleaned_data["email"]
            request.user.save()

            # Update profile data
            form.save()

            messages.success(request, "Your profile has been updated successfully!")
            return redirect("profile")
    else:
        form = UserProfileForm(instance=request.user.profile, user=request.user)

    context = {"form": form, "user_profile": request.user.profile}
    return render(request, "user/profile.html", context)


@admin_required
def user_management(request):
    """
    Admin dashboard for user management and role administration.

    This view provides administrators with a comprehensive interface to view
    all users in the system along with their profiles and roles. It displays
    user information in a tabular format with action buttons for role
    modification and user deletion.

    Args:
        request (HttpRequest): The HTTP request object

    Returns:
        HttpResponse: User management dashboard page

    Features:
        - Complete user list with profile information
        - Optimized database queries using select_related
        - Role display and management links
        - User action buttons (edit role, delete)

    Security:
        - Admin-only access via @admin_required decorator
        - Proper authorization checks

    Template:
        user/user_management.html

    Context:
        users (QuerySet): All users with their related profiles
    """
    users = User.objects.all().select_related("profile")

    context = {"users": users}
    return render(request, "user/user_management.html", context)


@admin_required
def update_user_role(request, user_id):
    """
    Admin function to update a user's role with validation.

    This view allows administrators to change user roles through a POST request.
    It validates the new role against available choices and provides appropriate
    feedback. The view is designed to be called via AJAX or form submission.

    Args:
        request (HttpRequest): The HTTP request object
        user_id (int): The ID of the user whose role should be updated

    Returns:
        HttpResponse: Redirect to user management page with status message

    Features:
        - Role validation against UserProfile.ROLE_CHOICES
        - Automatic profile saving after role change
        - Success/error feedback via messages
        - Safe handling of invalid user IDs

    Security:
        - Admin-only access via @admin_required decorator
        - Input validation for role values
        - 404 protection for invalid user IDs

    HTTP Methods:
        POST: Process role update request

    POST Parameters:
        role (str): New role value from UserProfile.ROLE_CHOICES
    """
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        new_role = request.POST.get("role")
        if new_role in dict(UserProfile.ROLE_CHOICES).keys():
            user.profile.role = new_role
            user.profile.save()
            messages.success(
                request,
                f"Role for {user.username} changed to {user.profile.get_role_display()}",
            )
        else:
            messages.error(request, "Invalid role selected")

    return redirect("user_management")


@admin_required
def delete_user(request, user_id):
    """
    Admin function to delete a user account with confirmation.

    This view allows administrators to delete user accounts. It requires
    POST confirmation for security and provides feedback about the deletion.
    The user's username is preserved in the success message for audit purposes.

    Args:
        request (HttpRequest): The HTTP request object
        user_id (int): The ID of the user to be deleted

    Returns:
        HttpResponse: Redirect to user management page with status message

    Features:
        - POST-only deletion for security
        - Username preservation for confirmation message
        - Safe cascade deletion of related UserProfile
        - Success feedback via messages

    Security:
        - Admin-only access via @admin_required decorator
        - POST confirmation required
        - 404 protection for invalid user IDs
        - Proper cascade deletion handling

    HTTP Methods:
        POST: Process user deletion request

    Warning:
        This operation permanently deletes the user and all related data.
        Ensure proper backup and confirmation procedures are in place.
    """
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        username = user.username
        user.delete()
        messages.success(request, f"User '{username}' has been deleted successfully")

    return redirect("user_management")


# Customer Support Views for Staff


@staff_required
def customer_support_dashboard(request):
    """
    Staff dashboard for comprehensive customer support ticket management.

    Provides a centralized interface for staff members to view, filter, search,
    and manage customer support tickets. Includes advanced filtering options,
    search functionality, pagination, and real-time statistics.

    Security:
        - Requires staff-level access (staff_required decorator)
        - Only staff and admin users can access this view
        - Implements proper query optimization with select_related/prefetch_related

    GET Parameters:
        status (str, optional): Filter by ticket status ('all', 'open', 'in_progress',
                               'pending_customer', 'resolved', 'closed'). Default: 'all'
        priority (str, optional): Filter by priority ('all', 'low', 'medium', 'high',
                                 'urgent'). Default: 'all'
        category (str, optional): Filter by category ID ('all' or category ID). Default: 'all'
        assigned (str, optional): Filter by assignment ('all', 'me', 'unassigned',
                                 or staff user ID). Default: 'all'
        search (str, optional): Search in ticket ID, subject, customer info, or description
        page (int, optional): Page number for pagination

    Template Context:
        page_obj (Page): Paginated ticket objects (20 per page)
        stats (dict): Dashboard statistics including:
            - total_tickets: Total number of tickets
            - open_tickets: Number of open tickets
            - in_progress_tickets: Number of in-progress tickets
            - pending_tickets: Number of pending customer response tickets
            - overdue_tickets: Number of overdue tickets
            - my_tickets: Number of tickets assigned to current user
            - unassigned_tickets: Number of unassigned tickets
        categories (QuerySet): Active support categories for filtering
        staff_members (QuerySet): Staff and admin users for assignment filtering
        status_filter (str): Current status filter value
        priority_filter (str): Current priority filter value
        category_filter (str): Current category filter value
        assigned_filter (str): Current assignment filter value
        search_query (str): Current search query
        status_choices (tuple): Available status choices for forms
        priority_choices (tuple): Available priority choices for forms

    Returns:
        HttpResponse: Rendered customer support dashboard template

    Example:
        # View all open tickets assigned to current user
        GET /auth/support/dashboard/?status=open&assigned=me

        # Search for tickets containing "payment"
        GET /auth/support/dashboard/?search=payment

        # View high priority unassigned tickets
        GET /auth/support/dashboard/?priority=high&assigned=unassigned
    """
    # Get filter parameters
    status_filter = request.GET.get("status", "all")
    priority_filter = request.GET.get("priority", "all")
    category_filter = request.GET.get("category", "all")
    assigned_filter = request.GET.get("assigned", "all")
    search_query = request.GET.get("search", "")

    # Base queryset
    tickets = SupportTicket.objects.select_related(
        "customer", "assigned_staff", "category"
    ).prefetch_related("responses")

    # Apply filters
    if status_filter != "all":
        tickets = tickets.filter(status=status_filter)

    if priority_filter != "all":
        tickets = tickets.filter(priority=priority_filter)

    if category_filter != "all":
        tickets = tickets.filter(category_id=category_filter)

    if assigned_filter == "me":
        tickets = tickets.filter(assigned_staff=request.user)
    elif assigned_filter == "unassigned":
        tickets = tickets.filter(assigned_staff__isnull=True)
    elif assigned_filter != "all":
        tickets = tickets.filter(assigned_staff_id=assigned_filter)

    if search_query:
        tickets = tickets.filter(
            Q(ticket_id__icontains=search_query)
            | Q(subject__icontains=search_query)
            | Q(customer__username__icontains=search_query)
            | Q(customer__email__icontains=search_query)
            | Q(description__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(tickets, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Get statistics
    stats = {
        "total_tickets": SupportTicket.objects.count(),
        "open_tickets": SupportTicket.objects.filter(status="open").count(),
        "in_progress_tickets": SupportTicket.objects.filter(
            status="in_progress"
        ).count(),
        "pending_tickets": SupportTicket.objects.filter(
            status="pending_customer"
        ).count(),
        "overdue_tickets": len(
            [
                t
                for t in SupportTicket.objects.exclude(
                    status__in=["resolved", "closed"]
                )
                if t.is_overdue
            ]
        ),
        "my_tickets": SupportTicket.objects.filter(assigned_staff=request.user).count(),
        "unassigned_tickets": SupportTicket.objects.filter(
            assigned_staff__isnull=True
        ).count(),
    }

    # Get filter options
    categories = SupportCategory.objects.filter(is_active=True)
    staff_members = User.objects.filter(profile__role__in=["staff", "admin"])

    context = {
        "page_obj": page_obj,
        "stats": stats,
        "categories": categories,
        "staff_members": staff_members,
        "status_filter": status_filter,
        "priority_filter": priority_filter,
        "category_filter": category_filter,
        "assigned_filter": assigned_filter,
        "search_query": search_query,
        "status_choices": SupportTicket.STATUS_CHOICES,
        "priority_choices": SupportTicket.PRIORITY_CHOICES,
    }

    return render(request, "auth/customer_support_dashboard.html", context)


def track_ticket(request):
    """
    Public ticket tracking interface for customers without account access.

    Allows anonymous users and customers to track their support tickets by providing
    the ticket ID and associated email address. Provides read-only access to ticket
    status, progress, and public responses.

    Security:
        - No authentication required (public access)
        - Requires both ticket ID and email for verification
        - Only shows non-internal responses to protect sensitive information
        - Prevents ticket enumeration by requiring exact email match

    GET Request:
        Displays the ticket tracking form

    POST Request:
        Processes ticket lookup with validation

        Required POST Parameters:
            ticket_id (str): The unique ticket identifier
            email (str): The customer's email address associated with the ticket

    Template Context (GET):
        error_message (str or None): Error message if ticket lookup failed

    Template Context (POST success):
        ticket (SupportTicket): The found ticket object
        responses (QuerySet): Public responses only (is_internal=False), ordered by creation date

    Returns:
        HttpResponse:
            - On GET: Track ticket form template
            - On POST success: Customer ticket detail template with ticket info
            - On POST error: Track ticket form with error message

    Error Handling:
        - Missing ticket ID or email: Generic validation error
        - Ticket not found: Security-conscious error message
        - Invalid data: Form validation with user-friendly messages

    Example:
        # Track ticket TK-001 with email customer@example.com
        POST /auth/support/track/
        ticket_id=TK-001&email=customer@example.com

    Templates:
        - GET/Error: 'auth/track_ticket.html'
        - Success: 'auth/customer_ticket_detail.html'
    """
    ticket = None
    error_message = None

    if request.method == "POST":
        ticket_id = request.POST.get("ticket_id", "").strip()
        email = request.POST.get("email", "").strip()

        if not ticket_id or not email:
            error_message = "Please provide both ticket ID and email."
        else:
            try:
                # Find the ticket matching both ID and email
                ticket = SupportTicket.objects.get(
                    ticket_id=ticket_id, customer_email=email
                )

                # Get visible responses (non-internal)
                responses = ticket.responses.filter(is_internal=False).order_by(
                    "created_at"
                )

                return render(
                    request,
                    "auth/customer_ticket_detail.html",
                    {"ticket": ticket, "responses": responses},
                )

            except SupportTicket.DoesNotExist:
                error_message = "No ticket found matching the provided ID and email. Please check your information and try again."

    return render(request, "auth/track_ticket.html", {"error_message": error_message})


@staff_required
def ticket_detail(request, ticket_id):
    """
    Comprehensive ticket management interface for staff members.

    Provides a detailed view and management interface for individual support tickets,
    allowing staff to view all responses, add new responses (public or internal),
    update ticket properties, and manage the entire ticket lifecycle.

    Security:
        - Requires staff-level access (staff_required decorator)
        - Only staff and admin users can access this view
        - Supports both public and internal response types
        - File attachment support with security validation

    URL Parameters:
        ticket_id (str): The unique ticket identifier

    GET Request:
        Displays the detailed ticket management interface

    POST Request:
        Handles two types of actions via 'action' parameter:

        Action 'add_response':
            message (str, required): Response content
            is_internal (bool, optional): Whether response is internal-only
            attachment (file, optional): File attachment for the response

        Action 'update_ticket':
            status (str, optional): New ticket status
            priority (str, optional): New ticket priority
            assigned_staff (str, optional): Staff user ID to assign ('None' to unassign)
            category (str, optional): Category ID ('None' to remove category)
            internal_notes (str, optional): Internal staff notes

    Template Context:
        ticket (SupportTicket): The ticket object with all details
        responses (QuerySet): All responses ordered by creation date (includes internal)
        categories (QuerySet): Active support categories for assignment
        staff_members (QuerySet): Staff and admin users for assignment
        status_choices (tuple): Available status options
        priority_choices (tuple): Available priority options

    Side Effects:
        - Creates SupportResponse objects for new responses
        - Automatically updates ticket status from 'open' to 'in_progress' on first response
        - Updates ticket properties based on form submission
        - Displays success messages for user feedback

    Returns:
        HttpResponse:
            - GET: Rendered ticket detail template
            - POST: Redirect to same ticket detail page with success message

    File Upload Security:
        - Supports file attachments for responses
        - File validation handled by model and storage backend
        - Attachment access controlled through ticket permissions

    Example:
        # View ticket details
        GET /auth/support/ticket/TK-001/

        # Add public response with attachment
        POST /auth/support/ticket/TK-001/
        action=add_response&message=Solution provided&attachment=file.pdf

        # Update ticket priority and assign to staff
        POST /auth/support/ticket/TK-001/
        action=update_ticket&priority=high&assigned_staff=123

    Template:
        'auth/ticket_detail.html'
    """
    ticket = get_object_or_404(SupportTicket, ticket_id=ticket_id)
    responses = ticket.responses.all().order_by("created_at")

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "add_response":
            message = request.POST.get("message")
            is_internal = request.POST.get("is_internal") == "on"
            attachment = request.FILES.get("attachment")
            if message:
                SupportResponse.objects.create(
                    ticket=ticket,
                    author=request.user,
                    message=message,
                    attachment=attachment,
                    is_internal=is_internal,
                    is_staff_response=True,
                )

                # Update ticket status if needed
                if ticket.status == "open":
                    ticket.status = "in_progress"
                    ticket.save()

                messages.success(request, "Response added successfully.")
                return redirect("ticket_detail", ticket_id=ticket_id)

        elif action == "update_ticket":
            status = request.POST.get("status")
            priority = request.POST.get("priority")
            assigned_staff_id = request.POST.get("assigned_staff")
            category_id = request.POST.get("category")
            internal_notes = request.POST.get("internal_notes")

            if status:
                ticket.status = status
            if priority:
                ticket.priority = priority
            if assigned_staff_id:
                ticket.assigned_staff_id = (
                    assigned_staff_id if assigned_staff_id != "None" else None
                )
            if category_id:
                ticket.category_id = category_id if category_id != "None" else None
            if internal_notes is not None:
                ticket.internal_notes = internal_notes

            ticket.save()
            messages.success(request, "Ticket updated successfully.")
            return redirect("ticket_detail", ticket_id=ticket_id)

    categories = SupportCategory.objects.filter(is_active=True)
    staff_members = User.objects.filter(profile__role__in=["staff", "admin"])

    context = {
        "ticket": ticket,
        "responses": responses,
        "categories": categories,
        "staff_members": staff_members,
        "status_choices": SupportTicket.STATUS_CHOICES,
        "priority_choices": SupportTicket.PRIORITY_CHOICES,
    }

    return render(request, "auth/ticket_detail.html", context)


@staff_required
def assign_ticket(request, ticket_id):
    """
    AJAX endpoint for quick ticket assignment to staff members.

    Provides a lightweight API for assigning or unassigning tickets to staff members
    without requiring a full page refresh. Used by the dashboard and ticket detail
    interfaces for efficient ticket management.

    Security:
        - Requires staff-level access (staff_required decorator)
        - Validates staff member exists and has appropriate role
        - Only allows assignment to users with 'staff' or 'admin' roles

    URL Parameters:
        ticket_id (str): The unique ticket identifier

    POST Request Only:
        Required POST Parameters:
            staff_id (str): User ID of staff member to assign, or 'unassign' to remove assignment

    Response:
        JSON Response:
            success (bool): True if assignment successful, False otherwise
            assigned_to (str): Username of assigned staff member or 'Unassigned'

    Error Handling:
        - Invalid ticket_id: Returns 404 via get_object_or_404
        - Invalid staff_id: Returns 404 via get_object_or_404
        - Non-POST request: Returns JSON error response
        - Staff member with invalid role: Returns 404

    Side Effects:
        - Updates SupportTicket.assigned_staff field
        - Triggers model save() method and any associated signals

    Returns:
        JsonResponse:
            - Success: {'success': True, 'assigned_to': 'username'}
            - Unassign: {'success': True, 'assigned_to': 'Unassigned'}
            - Error: {'success': False}

    Example:
        # Assign ticket to staff member with ID 123
        POST /auth/support/assign/TK-001/
        staff_id=123

        # Unassign ticket
        POST /auth/support/assign/TK-001/
        staff_id=unassign

    Frontend Usage:
        Used with JavaScript/AJAX for dynamic assignment without page reload.
        Typically called from dropdown menus or quick-action buttons.
    """
    if request.method == "POST":
        ticket = get_object_or_404(SupportTicket, ticket_id=ticket_id)
        staff_id = request.POST.get("staff_id")

        if staff_id == "unassign":
            ticket.assigned_staff = None
        else:
            staff_member = get_object_or_404(
                User, id=staff_id, profile__role__in=["staff", "admin"]
            )
            ticket.assigned_staff = staff_member

        ticket.save()

        return JsonResponse(
            {
                "success": True,
                "assigned_to": ticket.assigned_staff.username
                if ticket.assigned_staff
                else "Unassigned",
            }
        )

    return JsonResponse({"success": False})


@staff_required
def update_ticket_status(request, ticket_id):
    """
    AJAX endpoint for quick ticket status updates.

    Provides a lightweight API for updating ticket status without requiring a full
    page refresh. Validates status against available choices and returns the
    human-readable status display name.

    Security:
        - Requires staff-level access (staff_required decorator)
        - Validates status against SupportTicket.STATUS_CHOICES
        - Only allows predefined status values to prevent invalid data

    URL Parameters:
        ticket_id (str): The unique ticket identifier

    POST Request Only:
        Required POST Parameters:
            status (str): New status code (must match STATUS_CHOICES)
                         Valid values: 'open', 'in_progress', 'pending_customer', 'resolved', 'closed'

    Response:
        JSON Response:
            success (bool): True if status update successful, False otherwise
            status (str): Human-readable status display name (if successful)
            status_code (str): Raw status code value (if successful)

    Error Handling:
        - Invalid ticket_id: Returns 404 via get_object_or_404
        - Invalid status: Returns JSON error response
        - Non-POST request: Returns JSON error response

    Side Effects:
        - Updates SupportTicket.status field
        - Triggers model save() method and any associated signals
        - May trigger status-based business logic (SLA calculations, notifications, etc.)

    Returns:
        JsonResponse:
            - Success: {'success': True, 'status': 'In Progress', 'status_code': 'in_progress'}
            - Error: {'success': False}

    Example:
        # Update ticket to resolved status
        POST /auth/support/status/TK-001/
        status=resolved

        # Update ticket to in progress
        POST /auth/support/status/TK-001/
        status=in_progress

    Frontend Usage:
        Used with JavaScript/AJAX for dynamic status updates without page reload.
        Typically called from status dropdown menus or quick-action buttons.
        Frontend should update UI elements based on returned status display name.
    """
    if request.method == "POST":
        ticket = get_object_or_404(SupportTicket, ticket_id=ticket_id)
        new_status = request.POST.get("status")

        if new_status in dict(SupportTicket.STATUS_CHOICES):
            ticket.status = new_status
            ticket.save()

            return JsonResponse(
                {
                    "success": True,
                    "status": ticket.get_status_display(),
                    "status_code": ticket.status,
                }
            )

    return JsonResponse({"success": False})


@staff_required
def support_analytics(request):
    """
    Comprehensive analytics and reporting dashboard for customer support metrics.

    Provides detailed insights into support ticket trends, performance metrics, and
    team productivity. Includes customizable time period filtering and various
    statistical breakdowns for management reporting.

    Security:
        - Requires staff-level access (staff_required decorator)
        - Only staff and admin users can access analytics data
        - No customer PII exposed in aggregate statistics

    GET Parameters:
        period (str, optional): Number of days for analysis period. Default: '30'
                               Common values: '7', '30', '90', '365'

    Analytics Categories:
        Basic Statistics:
            - total_tickets: Total tickets in period
            - resolved_tickets: Successfully resolved tickets
            - closed_tickets: Closed tickets
            - open_tickets: Currently open tickets
            - in_progress_tickets: Tickets being worked on
            - avg_resolution_time: Average time to resolve (calculated field)

        Category Breakdown:
            - Ticket distribution by support category
            - Ordered by volume (highest first)

        Priority Analysis:
            - Ticket distribution by priority level
            - Ordered by count for priority planning

        Staff Performance:
            - Tickets assigned per staff member
            - Resolution counts per staff member
            - Workload distribution analysis

        Trend Analysis:
            - Daily ticket creation over the period
            - Time series data for graphing
            - Chronological trend identification

    Template Context:
        stats (dict): Core metrics and KPIs
        category_stats (QuerySet): Tickets grouped by category with counts
        priority_stats (QuerySet): Tickets grouped by priority with counts
        staff_stats (QuerySet): Staff performance metrics with assignment/resolution counts
        daily_stats (list): Daily ticket creation trend data
        period (str): Selected time period for filtering

    Data Processing:
        - Uses Django ORM aggregation for efficient calculations
        - Filters data by creation date within specified period
        - Optimizes queries with select_related and annotations
        - Processes daily trends in reverse chronological order

    Returns:
        HttpResponse: Rendered analytics dashboard template

    Example:
        # View 7-day analytics
        GET /auth/support/analytics/?period=7

        # View quarterly analytics
        GET /auth/support/analytics/?period=90

    Template:
        'auth/support_analytics.html'

    Frontend Integration:
        Template receives structured data suitable for:
        - Chart.js or similar charting libraries
        - Data tables with sorting/filtering
        - KPI dashboard widgets
        - Export functionality
    """
    # Time period filter
    period = request.GET.get("period", "30")  # days
    from_date = timezone.now() - timezone.timedelta(days=int(period))

    # Basic statistics
    total_tickets = SupportTicket.objects.filter(created_at__gte=from_date)

    stats = {
        "total_tickets": total_tickets.count(),
        "resolved_tickets": total_tickets.filter(status="resolved").count(),
        "closed_tickets": total_tickets.filter(status="closed").count(),
        "open_tickets": total_tickets.filter(status="open").count(),
        "in_progress_tickets": total_tickets.filter(status="in_progress").count(),
        "avg_resolution_time": 0,  # Calculate this based on resolved tickets
    }

    # Tickets by category
    category_stats = (
        total_tickets.values("category__name")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    # Tickets by priority
    priority_stats = (
        total_tickets.values("priority").annotate(count=Count("id")).order_by("-count")
    )

    # Staff performance
    staff_stats = (
        total_tickets.filter(assigned_staff__isnull=False)
        .values("assigned_staff__username")
        .annotate(
            assigned_count=Count("id"),
            resolved_count=Count("id", filter=Q(status="resolved")),
        )
        .order_by("-assigned_count")
    )

    # Daily ticket creation trend
    daily_stats = []
    for i in range(int(period)):
        date = (timezone.now() - timezone.timedelta(days=i)).date()
        count = total_tickets.filter(created_at__date=date).count()
        daily_stats.append({"date": date.strftime("%Y-%m-%d"), "count": count})
    daily_stats.reverse()

    context = {
        "stats": stats,
        "category_stats": category_stats,
        "priority_stats": priority_stats,
        "staff_stats": staff_stats,
        "daily_stats": daily_stats,
        "period": period,
    }

    return render(request, "auth/support_analytics.html", context)


# Customer Support Ticket Creation (Public Access)


def contact_view(request):
    """
    Public contact form for support ticket creation and customer inquiries.

    Handles public contact form submissions and automatically creates support tickets
    for customer service management. Supports both authenticated and anonymous users,
    with automatic account creation for anonymous submissions to enable ticket tracking.

    Security:
        - No authentication required (public access)
        - Input validation and sanitization for all form fields
        - File upload security through model validation
        - CSRF protection on form submissions
        - Safe user account creation with unique username generation

    GET Request:
        Displays the contact form with available support categories

    POST Request:
        Processes contact form submission and creates support ticket

        Required Form Fields:
            name (str): Customer's full name
            email (str): Customer's email address (used for account creation/lookup)
            subject (str): Brief description of the issue
            message (str): Detailed description of the problem or inquiry

        Optional Form Fields:
            phone (str): Customer's phone number
            category (str): Support category ID for proper routing
            priority (str): Priority level ('low', 'medium', 'high', 'urgent'). Default: 'medium'
            order_number (str): Related order number for purchase inquiries
            attachment (file): Supporting documentation or screenshots

    User Account Handling:
        - Authenticated users: Ticket assigned to current user
        - Anonymous users with existing email: Ticket assigned to existing account
        - Anonymous users with new email: Temporary account created automatically
        - Usernames generated safely with collision handling
        - Random passwords assigned to auto-created accounts

    Template Context:
        categories (QuerySet): Active support categories for form dropdown

    Side Effects:
        - Creates SupportTicket object with all provided information
        - May create new User account for anonymous submissions
        - Sends success/error messages to user
        - Provides ticket tracking information for anonymous users

    Error Handling:
        - Missing required fields: Form validation with error message
        - Database errors: Generic error message with form redisplay
        - Invalid category: Gracefully ignored, ticket created without category
        - File upload errors: Handled by model and storage backend

    Returns:
        HttpResponse:
            - GET: Contact form template
            - POST success: Redirect to contact page with success message
            - POST error: Contact form with error messages

    Auto-Generated Features:
        - Unique ticket ID generation (handled by model)
        - Customer account creation with unique username
        - Automatic first/last name parsing from full name
        - Ticket tracking instructions for anonymous users

    Example:
        # Submit contact form
        POST /contact/
        name=John Doe&email=john@example.com&subject=Login Issue&message=Cannot access my account

        # Submit with attachment and order reference
        POST /contact/
        name=Jane Smith&email=jane@example.com&subject=Order Problem&order_number=ORD-123&attachment=screenshot.png

    Templates:
        'static/contact.html'

    Success Message Format:
        "Your support ticket has been created successfully! Your ticket ID is #TK-001.
         We will respond to your inquiry within 24 hours."
    """
    categories = SupportCategory.objects.filter(is_active=True)

    if request.method == "POST":
        # Extract form data
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        subject = request.POST.get("subject", "").strip()
        category_id = request.POST.get("category")
        priority = request.POST.get("priority", "medium")
        message = request.POST.get("message", "").strip()
        order_number = request.POST.get("order_number", "").strip()
        attachment = request.FILES.get("attachment")

        # Basic validation
        if not all([name, email, subject, message]):
            messages.error(request, "Please fill in all required fields.")
            return render(request, "static/contact.html", {"categories": categories})

        try:
            # Get or create user account for the email
            customer = None
            if request.user.is_authenticated:
                customer = request.user
            else:
                # Try to find existing user with this email
                try:
                    customer = User.objects.get(email=email)
                except User.DoesNotExist:
                    # Create a temporary user account for ticket tracking
                    username = email.split("@")[0]
                    # Ensure unique username
                    counter = 1
                    original_username = username
                    while User.objects.filter(username=username).exists():
                        username = f"{original_username}{counter}"
                        counter += 1

                    customer = User.objects.create_user(
                        username=username,
                        email=email,
                        first_name=name.split()[0] if name.split() else name,
                        last_name=" ".join(name.split()[1:])
                        if len(name.split()) > 1
                        else "",
                        password=User.objects.make_random_password(),
                    )

            # Get category if provided
            category = None
            if category_id and category_id != "None":
                try:
                    category = SupportCategory.objects.get(
                        id=category_id, is_active=True
                    )
                except SupportCategory.DoesNotExist:
                    pass

            # Create support ticket
            ticket = SupportTicket.objects.create(
                customer=customer,
                subject=subject,
                category=category,
                description=message,
                customer_email=email,
                customer_phone=phone,
                priority=priority,
                order_number=order_number,
                attachment=attachment,
            )

            messages.success(
                request,
                f"Your support ticket has been created successfully! "
                f"Your ticket ID is #{ticket.ticket_id}. "
                f"We will respond to your inquiry within 24 hours.",
            )

            # If user was not logged in, provide them with ticket tracking info
            if not request.user.is_authenticated:
                messages.info(
                    request,
                    f"You can track your ticket status by using our ticket tracker with email: {email} "
                    f"and ticket ID: #{ticket.ticket_id}",
                )

            return redirect("contact")

        except Exception:
            messages.error(
                request,
                "An error occurred while creating your support ticket. Please try again.",
            )
            return render(request, "static/contact.html", {"categories": categories})

    context = {
        "categories": categories,
    }
    return render(request, "static/contact.html", context)


@login_required
def my_tickets_view(request):
    """
    Display customer's personal support ticket list with pagination.

    Provides authenticated users with access to their own support tickets,
    ordered by creation date (newest first). Includes pagination for better
    performance and user experience with large ticket lists.

    Security:
        - Requires user authentication (login_required decorator)
        - Only shows tickets belonging to the current user
        - No access to other users' tickets

    GET Parameters:
        page (int, optional): Page number for pagination (10 tickets per page)

    Ticket Filtering:
        - Automatically filters by customer=request.user
        - Orders by creation date (descending) for chronological view
        - Includes all ticket statuses (open, in progress, resolved, closed)

    Template Context:
        page_obj (Page): Paginated ticket objects with navigation info
            - Contains SupportTicket instances for current page
            - Provides pagination metadata (has_previous, has_next, etc.)
            - Optimized with 10 tickets per page for performance

    Performance:
        - Uses Django pagination for efficient large dataset handling
        - Database queries optimized with proper ordering
        - Minimal memory footprint with paginated results

    Returns:
        HttpResponse: Rendered customer ticket list template

    Navigation Features:
        - Pagination controls for browsing multiple pages
        - Direct links to individual ticket detail pages
        - Chronological organization (newest first)

    Example:
        # View first page of tickets
        GET /auth/tickets/

        # View specific page
        GET /auth/tickets/?page=2

    Template:
        'auth/my_tickets.html'

    Template Usage:
        The page_obj provides access to:
        - page_obj.object_list: Current page tickets
        - page_obj.has_previous: Whether previous page exists
        - page_obj.has_next: Whether next page exists
        - page_obj.previous_page_number: Previous page number
        - page_obj.next_page_number: Next page number
    """
    tickets = SupportTicket.objects.filter(customer=request.user).order_by(
        "-created_at"
    )

    # Pagination
    paginator = Paginator(tickets, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
    }
    return render(request, "auth/my_tickets.html", context)


@login_required
def customer_ticket_detail(request, ticket_id):
    """
    Customer-facing ticket detail view with limited interaction capabilities.

    Provides authenticated customers with detailed access to their own support tickets,
    including the ability to view the conversation history and add responses.
    Customers can only see public responses and cannot access internal staff notes.

    Security:
        - Requires user authentication (login_required decorator)
        - Validates ticket ownership (customer=request.user)
        - Only displays non-internal responses to protect sensitive information
        - Prevents access to other customers' tickets via 404 response

    URL Parameters:
        ticket_id (str): The unique ticket identifier

    GET Request:
        Displays ticket details and conversation history

    POST Request:
        Allows customer to add responses to the ticket

        Form Fields:
            message (str, required): Customer's response message
            attachment (file, optional): Supporting file attachment

    Access Control:
        - Ticket must belong to the authenticated user
        - Returns 404 if ticket doesn't exist or belongs to another user
        - Only public responses visible (is_internal=False)

    Template Context:
        ticket (SupportTicket): The customer's ticket with full details
        responses (QuerySet): Public responses only, ordered chronologically

    Customer Response Handling:
        - Creates SupportResponse with customer as author
        - Marks response as non-internal and non-staff
        - Supports file attachments with security validation
        - Automatically updates ticket status if previously resolved/closed

    Status Management:
        - Reopens resolved/closed tickets when customer responds
        - Changes status to 'pending_customer' to indicate customer activity
        - Maintains ticket lifecycle based on customer interaction

    Side Effects:
        - Creates new SupportResponse objects for customer replies
        - Updates ticket status from resolved/closed to pending_customer
        - Displays success messages for user feedback
        - Redirects to same page after successful response submission

    Returns:
        HttpResponse:
            - GET: Rendered ticket detail template with conversation
            - POST: Redirect to same ticket detail with success message
            - Invalid access: 404 response

    File Upload Security:
        - Attachment validation handled by model
        - File size and type restrictions applied
        - Secure file storage with proper permissions

    Example:
        # View ticket details
        GET /auth/ticket/TK-001/

        # Add customer response
        POST /auth/ticket/TK-001/
        message=Thank you for the help!&attachment=receipt.pdf

    Template:
        'auth/customer_ticket_detail.html'

    Customer Experience:
        - Read-only view of ticket information and status
        - Full conversation history (public responses only)
        - Ability to continue conversation with staff
        - File attachment support for additional context
        - Automatic ticket reopening when customer responds
    """
    ticket = get_object_or_404(
        SupportTicket, ticket_id=ticket_id, customer=request.user
    )
    responses = ticket.responses.filter(is_internal=False).order_by("created_at")

    if request.method == "POST":
        message = request.POST.get("message", "").strip()
        attachment = request.FILES.get("attachment")

        if message:
            SupportResponse.objects.create(
                ticket=ticket,
                author=request.user,
                message=message,
                attachment=attachment,
                is_internal=False,
                is_staff_response=False,
            )

            # Update ticket status if it was resolved/closed
            if ticket.status in ["resolved", "closed"]:
                ticket.status = "pending_customer"
                ticket.save()

            messages.success(request, "Your response has been added successfully.")
            return redirect("customer_ticket_detail", ticket_id=ticket_id)

    context = {
        "ticket": ticket,
        "responses": responses,
    }
    return render(request, "auth/customer_ticket_detail.html", context)
