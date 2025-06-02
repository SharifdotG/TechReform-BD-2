"""Django admin configuration for CartApp models.

This module configures the Django admin interface for cart and order management
models. It provides basic admin registration for all cart-related models to
enable easy management of shopping carts, orders, and shipping addresses through
the Django admin panel.

Registered Models:
- Cart: Shopping cart management for users and sessions
- CartItem: Individual items within shopping carts
- Order: Customer orders with complete order lifecycle
- OrderItem: Products within customer orders
- ShippingAddress: Delivery addresses for orders

The admin interface allows staff to:
- View and manage customer carts and cart items
- Track and update order status and payment information
- Review order history and customer purchase patterns
- Manage shipping addresses and delivery information
- Handle customer support and order-related issues

Usage:
Access through Django admin at /admin/ with appropriate permissions.
"""

from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem, ShippingAddress

# Register cart and checkout models for admin management
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
