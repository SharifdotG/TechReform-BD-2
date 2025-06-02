"""
URL configuration for the AuthApp Django application.

This module defines all URL patterns for authentication, user management, and
customer support functionality. The URLs are organized into logical groups
with appropriate access controls and naming conventions.

URL Groups:
    Authentication URLs:
        - login/: User login page
        - register/: User registration page
        - logout/: User logout functionality
        - profile/: User profile management

    User Management URLs (Admin/Staff only):
        - user-management/: User management dashboard
        - update-user-role/<int:user_id>/: Role modification for users
        - delete-user/<int:user_id>/: User account deletion

    Customer Support URLs (Staff only):
        - customer-support/: Staff support dashboard
        - customer-support/ticket/<str:ticket_id>/: Staff ticket detail view
        - customer-support/assign/<str:ticket_id>/: Ticket assignment
        - customer-support/update-status/<str:ticket_id>/: Status updates
        - customer-support/analytics/: Support analytics and reporting

    Customer Support URLs (Public Access):
        - contact/: Contact form for creating support tickets
        - my-tickets/: Customer's own ticket list
        - my-tickets/<str:ticket_id>/: Customer ticket detail view
        - track-ticket/: Public ticket tracking by ID

URL Naming Convention:
    - All URLs use descriptive names for reverse lookups
    - Staff-only URLs are prefixed with appropriate namespaces
    - Customer-facing URLs use simple, intuitive names

Access Control:
    - Authentication URLs: Public access
    - User management: Restricted to admin/staff roles
    - Staff support URLs: Restricted to staff/admin roles
    - Customer support URLs: Available to authenticated users

Examples:
    {% url 'login' %} - Generates login page URL
    {% url 'ticket_detail' ticket_id='TR12345678' %} - Staff ticket detail
    {% url 'customer_ticket_detail' ticket_id='TR12345678' %} - Customer view
"""

from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs - Public access for login/logout/registration
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    # User Management URLs - Admin/Staff access only
    path("user-management/", views.user_management, name="user_management"),
    path(
        "update-user-role/<int:user_id>/",
        views.update_user_role,
        name="update_user_role",
    ),
    path("delete-user/<int:user_id>/", views.delete_user, name="delete_user"),
    # Customer Support URLs - Staff/Admin access only
    path(
        "customer-support/",
        views.customer_support_dashboard,
        name="customer_support_dashboard",
    ),
    path(
        "customer-support/ticket/<str:ticket_id>/",
        views.ticket_detail,
        name="ticket_detail",
    ),
    path(
        "customer-support/assign/<str:ticket_id>/",
        views.assign_ticket,
        name="assign_ticket",
    ),
    path(
        "customer-support/update-status/<str:ticket_id>/",
        views.update_ticket_status,
        name="update_ticket_status",
    ),
    path(
        "customer-support/analytics/", views.support_analytics, name="support_analytics"
    ),
    # Customer Support URLs - Public/Customer access
    path("contact/", views.contact_view, name="contact"),
    path("my-tickets/", views.my_tickets_view, name="my_tickets"),
    path(
        "my-tickets/<str:ticket_id>/",
        views.customer_ticket_detail,
        name="customer_ticket_detail",
    ),
    path("track-ticket/", views.track_ticket, name="track_ticket"),
]
