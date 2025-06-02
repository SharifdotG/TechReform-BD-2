"""View functions for CartApp shopping cart and order management.

This module contains all view functions for handling shopping cart operations,
checkout processes, order management, and administrative order handling in the
TechReform e-commerce application. It provides comprehensive cart functionality
for both authenticated and anonymous users.

Key Features:
- Session-based cart management for anonymous users
- User account integration for registered customers
- Multi-category product support with dynamic model mapping
- Complete checkout and order processing workflow
- Order history and tracking for customers
- Administrative order management and status updates
- AJAX-powered cart updates for smooth user experience

View Categories:
- Cart Operations: add_to_cart, update_cart, remove_from_cart, view_cart
- Checkout Process: checkout, order_complete
- Order Management: my_orders, order_detail
- Admin Functions: admin_order_management, admin_order_detail, update_order_status

The module integrates with ProductsApp models through dynamic model mapping
to support all product categories (CPU, GPU, RAM, etc.) in a unified cart system.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.core.paginator import Paginator
from decimal import Decimal
import uuid

from .models import Cart, CartItem, Order, OrderItem, ShippingAddress
from AuthApp.decorators import staff_required
from ProductsApp.models import (
    CPU,
    Cooler,
    Motherboard,
    RAM,
    SSD,
    HDD,
    GPU,
    PowerSupply,
    Casing,
    Monitor,
    Keyboard,
    Mouse,
    Headphone,
)


def get_cart(request):
    """Get or create a cart for the current user or session.

    Handles cart retrieval for both authenticated and anonymous users.
    For authenticated users, creates or retrieves a user-linked cart.
    For anonymous users, uses session-based cart identification.

    Args:
        request (HttpRequest): The HTTP request object containing user
                              and session information

    Returns:
        Cart: The cart instance for the current user/session

    Session Management:
        - Creates unique session ID for anonymous users if not present
        - Maintains cart persistence across browser sessions
        - Handles cart migration when anonymous user logs in

    Example:
        >>> cart = get_cart(request)
        >>> cart.get_cart_total
        Decimal('299.99')
    """
    if request.user.is_authenticated:
        # If user is logged in, get or create their cart
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # If anonymous user, use session ID to track cart
        session_id = request.session.get("cart_session_id")
        if not session_id:
            session_id = str(uuid.uuid4())
            request.session["cart_session_id"] = session_id
            # Make sure session is saved
            request.session.modified = True

        cart, created = Cart.objects.get_or_create(session_id=session_id)

    return cart


def get_product_by_category(category, product_id):
    """Get a product instance based on category and ID.

    Uses dynamic model mapping to retrieve a product from the appropriate
    ProductsApp model based on the category name. Supports all product
    categories available in the TechReform system.

    Args:
        category (str): Product category name (e.g., 'CPU', 'GPU', 'RAM')
        product_id (str): UUID of the product to retrieve

    Returns:
        Model instance or None: The product object if found, None if not found
                               or if category is invalid

    Supported Categories:
        CPU, Cooler, Motherboard, RAM, SSD, HDD, GPU, Power Supply,
        Casing, Monitor, Keyboard, Mouse, Headphone

    Example:
        >>> product = get_product_by_category('CPU', 'some-uuid')
        >>> print(product.name)
        'Intel Core i7-12700K'
    """
    model_dict = {
        "CPU": CPU,
        "Cooler": Cooler,
        "Motherboard": Motherboard,
        "RAM": RAM,
        "SSD": SSD,
        "HDD": HDD,
        "GPU": GPU,
        "Power Supply": PowerSupply,
        "Casing": Casing,
        "Monitor": Monitor,
        "Keyboard": Keyboard,
        "Mouse": Mouse,
        "Headphone": Headphone,
    }

    if category in model_dict:
        model = model_dict[category]
        try:
            return model.objects.get(id=product_id)
        except model.DoesNotExist:
            return None
    return None


def add_to_cart(request):
    """Add a product to the shopping cart.

    Handles adding products from any category to the user's cart with
    quantity and stock validation. Supports both AJAX and form submissions.
    Updates existing cart items or creates new ones as needed.

    Args:
        request (HttpRequest): POST request containing:
                              - product_id: UUID of the product to add
                              - product_category: Category name for model lookup
                              - quantity: Number of items to add (default: 1)

    Returns:
        JsonResponse: JSON response containing:
                     - status: 'success' or 'error'
                     - message: User-friendly status message
                     - cart_count: Updated total items in cart
                     - cart_subtotal: Updated cart total price

    Validation:
        - Verifies product exists and is available
        - Checks stock availability before adding
        - Prevents adding more than available stock

    Example:
        POST data: {
            'product_id': 'some-uuid',
            'product_category': 'CPU',
            'quantity': '2'
        }

        Response: {
            'status': 'success',
            'message': 'Product added to cart',
            'cart_count': 3,
            'cart_subtotal': '899.98'
        }
    """
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product_category = request.POST.get("product_category")
        quantity = int(request.POST.get("quantity", 1))

        # Get the product
        product = get_product_by_category(product_category, product_id)
        if not product:
            return JsonResponse({"status": "error", "message": "Product not found"})

        # Check stock
        if quantity > product.stock:
            return JsonResponse(
                {"status": "error", "message": "Not enough stock available"}
            )

        # Get or create cart
        cart = get_cart(request)

        # Check if item already in cart
        try:
            cart_item = CartItem.objects.get(
                cart=cart, product_id=product_id, product_category=product_category
            )
            # Update quantity if already in cart
            cart_item.quantity += quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            # Create new cart item
            CartItem.objects.create(
                cart=cart,
                product_id=product_id,
                product_category=product_category,
                quantity=quantity,
                price=product.price,
            )  # Return success response
        messages.success(request, f"{product.brand} {product.model} added to cart.")
        return JsonResponse(
            {
                "status": "success",
                "message": "Product added to cart",
                "cart_count": cart.get_cart_items_count,
                "cart_subtotal": cart.get_cart_total,  # Add the cart subtotal to the response
            }
        )

    return JsonResponse({"status": "error", "message": "Invalid request"})


def update_cart(request):
    """Update the quantity of an item in the cart.

    Allows users to modify the quantity of products already in their cart.
    Includes stock validation and supports removing items by setting quantity to 0.
    Ensures security by verifying cart ownership.

    Args:
        request (HttpRequest): POST request containing:
                              - item_id: UUID of the cart item to update
                              - quantity: New quantity (0 to remove item)

    Returns:
        JsonResponse: JSON response containing:
                     - status: 'success' or 'error'
                     - message: User-friendly status message
                     - cart_count: Updated total items in cart
                     - cart_total: Updated cart total price
                     - item_total: Updated total for the specific item

    Security:
        - Verifies cart item belongs to current user/session
        - Validates stock availability before updating
        - Prevents unauthorized cart modifications

    Example:
        POST data: {
            'item_id': 'cart-item-uuid',
            'quantity': '3'
        }

        Response: {
            'status': 'success',
            'message': 'Cart updated',
            'cart_count': 5,
            'cart_total': '1299.97',
            'item_total': '899.97'
        }
    """
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        quantity = int(request.POST.get("quantity", 1))

        # Get the cart item
        try:
            cart_item = CartItem.objects.get(id=item_id)
            # Ensure the cart belongs to the current user or session
            cart = get_cart(request)
            if cart_item.cart != cart:
                return JsonResponse(
                    {"status": "error", "message": "Cart item not found"}
                )

            # Check product stock
            product = get_product_by_category(
                cart_item.product_category, cart_item.product_id
            )
            if product and quantity > product.stock:
                return JsonResponse(
                    {"status": "error", "message": "Not enough stock available"}
                )

            # Update quantity
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
            else:
                cart_item.delete()

            # Return updated cart data
            cart = get_cart(request)
            return JsonResponse(
                {
                    "status": "success",
                    "message": "Cart updated",
                    "cart_count": cart.get_cart_items_count,
                    "cart_total": cart.get_cart_total,
                    "item_total": cart_item.get_total if quantity > 0 else 0,
                }
            )

        except CartItem.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Cart item not found"})

    return JsonResponse({"status": "error", "message": "Invalid request"})


def remove_from_cart(request):
    """Remove an item completely from the cart.

    Permanently removes a cart item and returns updated cart totals.
    Includes security validation to ensure users can only remove items
    from their own carts.

    Args:
        request (HttpRequest): POST request containing:
                              - item_id: UUID of the cart item to remove

    Returns:
        JsonResponse: JSON response containing:
                     - status: 'success' or 'error'
                     - message: User-friendly status message
                     - cart_count: Updated total items in cart
                     - cart_total: Updated cart total price

    Security:
        - Verifies cart item belongs to current user/session
        - Prevents unauthorized item removal

    Example:
        POST data: {
            'item_id': 'cart-item-uuid'
        }

        Response: {
            'status': 'success',
            'message': 'Item removed from cart',
            'cart_count': 2,
            'cart_total': '399.98'
        }
    """
    if request.method == "POST":
        item_id = request.POST.get("item_id")

        # Get the cart item
        try:
            cart_item = CartItem.objects.get(id=item_id)
            # Ensure the cart belongs to the current user or session
            cart = get_cart(request)
            if cart_item.cart != cart:
                return JsonResponse(
                    {"status": "error", "message": "Cart item not found"}
                )

            # Delete the cart item
            cart_item.delete()

            # Return updated cart data
            return JsonResponse(
                {
                    "status": "success",
                    "message": "Item removed from cart",
                    "cart_count": cart.get_cart_items_count,
                    "cart_total": cart.get_cart_total,
                }
            )

        except CartItem.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Cart item not found"})

    return JsonResponse({"status": "error", "message": "Invalid request"})


def view_cart(request):
    """Display the cart contents"""
    cart = get_cart(request)
    cart_items = cart.cartitem_set.all()

    # Get the actual product instances for each cart item
    for item in cart_items:
        product = get_product_by_category(item.product_category, item.product_id)
        item.product = product

    context = {
        "cart": cart,
        "cart_items": cart_items,
    }

    return render(request, "cart/cart.html", context)


@login_required
def checkout(request):
    """Process checkout"""
    cart = get_cart(request)
    cart_items = cart.cartitem_set.all()

    # If cart is empty, redirect to cart page
    if cart_items.count() == 0:
        messages.warning(request, "Your cart is empty.")
        return redirect("view_cart")

    # Get the actual product instances for each cart item
    for item in cart_items:
        product = get_product_by_category(item.product_category, item.product_id)
        item.product = product

        # Check product stock
        if product and item.quantity > product.stock:
            messages.warning(
                request,
                f"Not enough stock for {product.brand} {product.model}. Only {product.stock} available.",
            )
            return redirect("view_cart")

    # Process the order
    if request.method == "POST":
        # Get shipping information
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address_line1 = request.POST.get("address_line1")
        address_line2 = request.POST.get("address_line2", "")
        city = request.POST.get("city")
        state = request.POST.get("state")
        postal_code = request.POST.get("postal_code")
        payment_method = request.POST.get("payment_method", "cash_on_delivery")
        notes = request.POST.get("notes", "")

        # Validate required fields
        if not all([full_name, email, phone, address_line1, city, state, postal_code]):
            messages.error(request, "Please fill in all required fields.")
            return redirect("checkout")

        # Calculate shipping cost (could be based on location, weight, etc.)
        shipping_cost = Decimal("150.00")  # Default shipping cost

        # Calculate subtotal
        subtotal = cart.get_cart_total

        # Create the order
        order = Order.objects.create(
            user=request.user,
            payment_method=payment_method,
            shipping_cost=shipping_cost,
            total_price=subtotal + shipping_cost,  # Remove tax from total
            notes=notes,
            ip_address=request.META.get("REMOTE_ADDR", ""),
        )

        # Create shipping address
        ShippingAddress.objects.create(
            order=order,
            user=request.user,
            full_name=full_name,
            phone=phone,
            email=email,
            address_line1=address_line1,
            address_line2=address_line2,
            city=city,
            state=state,
            postal_code=postal_code,
        )

        # Create order items and adjust inventory
        for item in cart_items:
            product = get_product_by_category(item.product_category, item.product_id)
            if product:
                # Create order item
                OrderItem.objects.create(
                    order=order,
                    product_id=item.product_id,
                    product_category=item.product_category,
                    product_name=f"{product.brand} {product.model}",
                    quantity=item.quantity,
                    price=item.price,
                )

                # Adjust inventory
                product.stock -= item.quantity
                product.save()

        # Clear the cart
        cart_items.delete()

        # Redirect to order confirmation
        return redirect("order_complete", order_id=order.id)

    # Calculate shipping for display
    subtotal = cart.get_cart_total
    shipping = Decimal("150.00")  # Default shipping
    grand_total = subtotal + shipping

    context = {
        "cart": cart,
        "cart_items": cart_items,
        "subtotal": subtotal,
        "shipping": shipping,
        "grand_total": grand_total,
    }

    return render(request, "cart/checkout.html", context)


@login_required
def order_complete(request, order_id):
    """Display order confirmation"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.orderitem_set.all()

    context = {
        "order": order,
        "order_items": order_items,
    }

    return render(request, "cart/order-confirmation.html", context)


@login_required
def my_orders(request):
    """Display user's order history"""
    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    context = {
        "orders": orders,
    }

    return render(request, "cart/my-orders.html", context)


@login_required
def order_detail(request, order_id):
    """Display detailed view of a specific order"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.orderitem_set.all()
    shipping_address = order.shipping_address

    context = {
        "order": order,
        "order_items": order_items,
        "shipping_address": shipping_address,
    }

    return render(request, "cart/order-detail.html", context)


# Admin Order Management Views

@staff_required
def admin_order_management(request):
    """Admin dashboard for order management"""
    # Get order statistics
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    processing_orders = Order.objects.filter(status='processing').count()
    shipped_orders = Order.objects.filter(status='shipped').count()
    completed_orders = Order.objects.filter(status='delivered').count()

    # Get total revenue from delivered orders
    total_revenue = Order.objects.filter(status='delivered').aggregate(
        total=Sum('total_price')
    )['total'] or Decimal('0.00')

    # Get recent orders
    recent_orders = Order.objects.all().order_by('-created_at')[:10]

    # Get orders by status for filtering
    status_filter = request.GET.get('status', 'all')
    if status_filter == 'all':
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(status=status_filter)

    # Pagination
    paginator = Paginator(orders.order_by('-created_at'), 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'processing_orders': processing_orders,
        'shipped_orders': shipped_orders,
        'completed_orders': completed_orders,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
        'page_obj': page_obj,
        'status_filter': status_filter,
        'orders': page_obj,
    }

    return render(request, 'cart/admin_order_management.html', context)


@staff_required
def admin_order_detail(request, order_id):
    """Admin view for order details with status update capability"""
    order = get_object_or_404(Order, id=order_id)
    order_items = order.orderitem_set.all()
    shipping_address = order.shipping_address

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_status':
            new_status = request.POST.get('status')
            if new_status in [choice[0] for choice in Order.STATUS_CHOICES]:
                order.status = new_status
                order.save()
                messages.success(request, f'Order status updated to {new_status.title()}')
                return redirect('admin_order_detail', order_id=order.id)

        elif action == 'update_payment':
            payment_status = request.POST.get('payment_status')
            if payment_status in [choice[0] for choice in Order.PAYMENT_STATUS_CHOICES]:
                order.payment_status = payment_status
                order.save()
                messages.success(request, f'Payment status updated to {payment_status.replace("_", " ").title()}')
                return redirect('admin_order_detail', order_id=order.id)

    context = {
        'order': order,
        'order_items': order_items,
        'shipping_address': shipping_address,
        'status_choices': Order.STATUS_CHOICES,
        'payment_choices': Order.PAYMENT_STATUS_CHOICES,
    }

    return render(request, 'cart/admin_order_detail.html', context)


@staff_required
def update_order_status(request):
    """AJAX endpoint to update order status"""
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')

        try:
            order = Order.objects.get(id=order_id)
            if new_status in [choice[0] for choice in Order.STATUS_CHOICES]:
                order.status = new_status
                order.save()
                return JsonResponse({
                    'status': 'success',
                    'message': f'Order status updated to {new_status.title()}'
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid status'
                })
        except Order.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Order not found'
            })

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    })
