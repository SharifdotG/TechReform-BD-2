"""URL configuration for CartApp views.

This module defines URL patterns for the shopping cart and order management
functionality of the TechReform e-commerce application. It provides routes
for cart operations, checkout process, order management, and administrative
order handling.

URL Patterns:
- Cart Management: Add, update, remove items and view cart
- Checkout Process: Complete purchase and order confirmation
- Order Tracking: View order history and details
- Admin Functions: Order management and status updates

The URLs support both customer-facing cart operations and administrative
order management functions with appropriate access controls.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Cart Management URLs
    path("add/", views.add_to_cart, name="add_to_cart"),  # Add product to cart
    path("update/", views.update_cart, name="update_cart"),  # Update item quantity
    path("remove/", views.remove_from_cart, name="remove_from_cart"),  # Remove item
    path("", views.view_cart, name="view_cart"),  # Display cart contents

    # Checkout and Order Processing URLs
    path("checkout/", views.checkout, name="checkout"),  # Checkout process
    path(
        "order/complete/<uuid:order_id>/",
        views.order_complete,
        name="order_complete"
    ),  # Order confirmation page

    # Customer Order Management URLs
    path("my-orders/", views.my_orders, name="my_orders"),  # User order history
    path("order/<uuid:order_id>/", views.order_detail, name="order_detail"),  # Order details

    # Administrative Order Management URLs (Staff Only)
    path("admin/orders/", views.admin_order_management, name="admin_order_management"),  # Order list
    path("admin/order/<uuid:order_id>/", views.admin_order_detail, name="admin_order_detail"),  # Admin order view
    path("admin/update-status/", views.update_order_status, name="update_order_status"),  # Status updates
]
