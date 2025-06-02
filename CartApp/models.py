"""Django models for the CartApp.

This module defines the database models for the shopping cart and order
management functionality of the TechReform e-commerce application. It provides
a complete order processing system with session-based cart management, user
account integration, and comprehensive order tracking.

The models include:
- Cart: Shopping cart for both authenticated and anonymous users
- CartItem: Individual items within a shopping cart
- Order: Customer orders with status tracking and payment information
- OrderItem: Individual products within an order
- ShippingAddress: Delivery address information for orders

The system supports:
- Session-based carts for anonymous users
- User-account linked carts for registered customers
- Multi-category product integration via dynamic model mapping
- Complete order lifecycle from cart to delivery
- Multiple payment methods and status tracking
- Comprehensive shipping address management

All models use UUID primary keys for enhanced security and scalability.
"""

from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone


class Cart(models.Model):
    """Shopping cart model for managing user cart items.

    Supports both authenticated and anonymous users through either user account
    linking or session-based identification. Each cart can contain multiple items
    and provides methods for calculating totals, item counts, and shipping weights.

    Attributes:
        id (UUIDField): Unique identifier for the cart
        user (OneToOneField): Optional link to authenticated user
        session_id (CharField): Session identifier for anonymous users
        created_at (DateTimeField): Cart creation timestamp
        updated_at (DateTimeField): Last modification timestamp

    Related Models:
        - CartItem: Individual items within this cart
        - User: Cart owner (optional for anonymous carts)

    Usage:
        # For authenticated users
        cart = Cart.objects.get(user=request.user)

        # For anonymous users
        cart = Cart.objects.get(session_id=request.session.session_key)
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="cartapp_cart",
    )
    session_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return string representation of the cart."""
        return f"Cart {self.id}"

    @property
    def get_cart_total(self):
        """Calculate total price of all items in cart.

        Iterates through all cart items and sums their individual totals
        (quantity * price) to get the cart subtotal.

        Returns:
            decimal.Decimal: Total price of all items in cart

        Example:
            >>> cart = Cart.objects.get(id='some-uuid')
            >>> cart.get_cart_total
            Decimal('599.99')
        """
        cart_items = self.cartitem_set.all()
        total = sum(item.get_total for item in cart_items)
        return total

    @property
    def get_cart_items_count(self):
        """Get total count of all items in cart.

        Sums the quantity of all cart items to get the total
        number of individual products in the cart.

        Returns:
            int: Total quantity of all items in cart

        Example:
            >>> cart = Cart.objects.get(id='some-uuid')
            >>> cart.get_cart_items_count
            7
        """
        cart_items = self.cartitem_set.all()
        total = sum(item.quantity for item in cart_items)
        return total

    @property
    def get_cart_weight(self):
        """Calculate total weight for shipping calculation.

        This method is prepared for future implementation of weight-based
        shipping calculations. Currently returns 0 as product weights
        are not yet implemented.

        Returns:
            int: Total weight of cart items (currently 0)

        Note:
            This will be implemented when product weight attributes are added
            to the product models in ProductsApp.
        """
        # This can be implemented later based on product weights
        return 0


class CartItem(models.Model):
    """Individual item within a shopping cart.

    Represents a specific product added to a cart with quantity and price
    information. Uses dynamic product model mapping to support all product
    categories available in the ProductsApp.

    Attributes:
        id (UUIDField): Unique identifier for the cart item
        cart (ForeignKey): Reference to the cart containing this item
        product_id (UUIDField): ID of the product from any category model
        product_category (CharField): Product category name for model lookup
        quantity (PositiveIntegerField): Number of this product in cart
        price (DecimalField): Price per unit at time of adding to cart
        created_at (DateTimeField): Item creation timestamp
        updated_at (DateTimeField): Last modification timestamp

    Related Models:
        - Cart: The cart containing this item
        - ProductsApp models: CPU, GPU, RAM, etc. (dynamic relationship)

    Usage:
        # Add item to cart
        cart_item = CartItem.objects.create(
            cart=cart,
            product_id=product.id,
            product_category='CPU',
            quantity=1,
            price=product.price
        )
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product_id = models.UUIDField()
    product_category = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return string representation of the cart item."""
        return f"{self.quantity} x {self.product_category} in Cart {self.cart.id}"

    @property
    def get_total(self):
        """Calculate total price for this cart item.

        Multiplies the unit price by quantity to get the subtotal
        for this specific item.

        Returns:
            decimal.Decimal: Total price for this item (price * quantity)

        Example:
            >>> item = CartItem.objects.get(id='some-uuid')
            >>> item.price = Decimal('299.99')
            >>> item.quantity = 2
            >>> item.get_total
            Decimal('599.98')
        """
        return self.price * self.quantity

    def get_product(self):
        """Get the actual product instance from appropriate model.

        Uses dynamic model mapping to retrieve the product object from
        the correct ProductsApp model based on the product_category field.

        Returns:
            Model instance or None: The product object if found, None otherwise

        Raises:
            None: Returns None if product category is invalid or product
                  doesn't exist instead of raising exceptions

        Example:
            >>> item = CartItem.objects.get(id='some-uuid')
            >>> item.product_category = 'CPU'
            >>> product = item.get_product()
            >>> print(product.name)
            'Intel Core i7-12700K'
        """
        # Dynamically import the model based on the category
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

        if self.product_category in model_dict:
            model = model_dict[self.product_category]
            try:
                return model.objects.get(id=self.product_id)
            except model.DoesNotExist:
                return None
        return None


class Order(models.Model):
    """Customer order model with complete order lifecycle management.

    Represents a customer order from cart checkout through delivery. Includes
    comprehensive status tracking, payment management, shipping calculations,
    and order history. Supports both authenticated and guest orders.

    Attributes:
        id (UUIDField): Unique identifier for the order
        user (ForeignKey): Optional link to user account (null for guest orders)
        order_number (CharField): Human-readable unique order identifier
        status (CharField): Current order status (pending, processing, shipped, etc.)
        payment_method (CharField): Selected payment method
        payment_status (CharField): Current payment status
        tax (DecimalField): Tax amount (currently not used, defaults to 0)
        shipping_cost (DecimalField): Shipping charges
        total_price (DecimalField): Final order total including all charges
        notes (TextField): Optional order notes or special instructions
        ip_address (CharField): Customer IP address for security tracking
        created_at (DateTimeField): Order creation timestamp
        updated_at (DateTimeField): Last modification timestamp
        payment_date (DateTimeField): Payment completion timestamp
        shipped_date (DateTimeField): Shipping dispatch timestamp
        delivered_date (DateTimeField): Delivery completion timestamp

    Status Choices:
        - pending: Order received, awaiting processing
        - processing: Order being prepared
        - shipped: Order dispatched for delivery
        - delivered: Order successfully delivered
        - cancelled: Order cancelled

    Payment Methods:
        - cash_on_delivery: Cash payment upon delivery
        - credit_card: Credit card payment
        - debit_card: Debit card payment
        - bkash: bKash mobile payment
        - nagad: Nagad mobile payment
        - rocket: Rocket mobile payment

    Payment Status:
        - pending: Payment not yet processed
        - paid: Payment completed successfully
        - failed: Payment attempt failed
        - refunded: Payment refunded to customer

    Related Models:
        - OrderItem: Individual products within this order
        - ShippingAddress: Delivery address for this order
        - User: Order customer (optional)

    Usage:
        # Create new order from cart
        order = Order.objects.create(
            user=request.user,
            payment_method='cash_on_delivery',
            total_price=cart.get_cart_total
        )
    """

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    )

    PAYMENT_CHOICES = (
        ("cash_on_delivery", "Cash on Delivery"),
        ("credit_card", "Credit Card"),
        ("debit_card", "Debit Card"),
        ("bkash", "bKash"),
        ("nagad", "Nagad"),
        ("rocket", "Rocket"),
    )

    PAYMENT_STATUS_CHOICES = (
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cartapp_orders",
    )
    order_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_CHOICES, default="cash_on_delivery"
    )
    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS_CHOICES, default="pending"
    )
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True, null=True)
    ip_address = models.CharField(max_length=20, blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_date = models.DateTimeField(blank=True, null=True)
    shipped_date = models.DateTimeField(blank=True, null=True)
    delivered_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        """Return string representation of the order."""
        return self.order_number

    def save(self, *args, **kwargs):
        """Override save method to auto-generate order number.

        Automatically generates a unique order number using timestamp
        if one is not already provided. Format: TR{timestamp}

        Args:
            *args: Positional arguments passed to parent save method
            **kwargs: Keyword arguments passed to parent save method

        Example:
            >>> order = Order()
            >>> order.save()
            >>> print(order.order_number)
            'TR1703123456'
        """
        # Generate order number if not provided
        if not self.order_number:
            timestamp = int(timezone.now().timestamp())
            self.order_number = f"TR{timestamp}"
        super().save(*args, **kwargs)

    @property
    def get_order_total(self):
        """Calculate order subtotal from all order items.

        Sums the total price of all individual order items
        (item price * quantity) to get the order subtotal
        before shipping and tax.

        Returns:
            decimal.Decimal: Order subtotal before shipping and tax

        Example:
            >>> order = Order.objects.get(order_number='TR1703123456')
            >>> order.get_order_total
            Decimal('1299.98')
        """
        order_items = self.orderitem_set.all()
        return sum(item.get_total for item in order_items)

    @property
    def get_grand_total(self):
        """Calculate final order total including shipping.

        Adds shipping cost to the order subtotal to get the final
        amount the customer pays. Tax is not currently implemented
        but the structure is prepared for future tax calculations.

        Returns:
            decimal.Decimal: Final order total including shipping

        Example:
            >>> order = Order.objects.get(order_number='TR1703123456')
            >>> order.get_grand_total
            Decimal('1349.98')  # includes shipping
        """
        return self.get_order_total + self.shipping_cost


class OrderItem(models.Model):
    """Individual product item within a customer order.

    Represents a specific product purchased in an order with quantity,
    price, and product details frozen at order time. Unlike CartItem,
    OrderItem stores the product name directly to preserve order history
    even if the original product is modified or deleted.

    Attributes:
        id (UUIDField): Unique identifier for the order item
        order (ForeignKey): Reference to the parent order
        product_id (UUIDField): Original product ID for reference
        product_category (CharField): Product category for classification
        product_name (CharField): Product name frozen at order time
        quantity (PositiveIntegerField): Number of this product ordered
        price (DecimalField): Price per unit at time of purchase
        created_at (DateTimeField): Item creation timestamp

    Related Models:
        - Order: The order containing this item
        - ProductsApp models: Original product references (via product_id)

    Usage:
        # Create order item from cart item
        order_item = OrderItem.objects.create(
            order=order,
            product_id=cart_item.product_id,
            product_category=cart_item.product_category,
            product_name=product.name,
            quantity=cart_item.quantity,
            price=cart_item.price
        )
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.UUIDField()
    product_category = models.CharField(max_length=50)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return string representation of the order item."""
        return (
            f"{self.quantity} x {self.product_name} in Order {self.order.order_number}"
        ) @ property

    def get_total(self):
        """Calculate total price for this order item.

        Multiplies the unit price by quantity to get the total
        cost for this specific item in the order.

        Returns:
            decimal.Decimal: Total price for this item (price * quantity)

        Example:
            >>> item = OrderItem.objects.get(id='some-uuid')
            >>> item.price = Decimal('599.99')
            >>> item.quantity = 2
            >>> item.get_total
            Decimal('1199.98')
        """
        return self.price * self.quantity


class ShippingAddress(models.Model):
    """Delivery address information for customer orders.

    Stores complete shipping address details for order delivery.
    Each order has exactly one shipping address, and the model also
    maintains a reference to the user for address history and reuse.

    Attributes:
        id (UUIDField): Unique identifier for the shipping address
        order (OneToOneField): The order this address belongs to
        user (ForeignKey): Optional user reference for address history
        full_name (CharField): Recipient's full name
        phone (CharField): Contact phone number
        email (EmailField): Contact email address
        address_line1 (CharField): Primary address line (street, building)
        address_line2 (CharField): Secondary address line (apartment, unit)
        city (CharField): City name
        state (CharField): State or province name
        postal_code (CharField): ZIP or postal code
        created_at (DateTimeField): Address creation timestamp
        updated_at (DateTimeField): Last modification timestamp

    Related Models:
        - Order: The order being shipped to this address
        - User: Address owner for history tracking (optional)

    Usage:
        # Create shipping address for order
        address = ShippingAddress.objects.create(
            order=order,
            user=request.user,
            full_name='John Doe',
            phone='+8801234567890',
            email='john@example.com',
            address_line1='123 Main Street',
            city='Dhaka',
            state='Dhaka',
            postal_code='1000'
        )
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="shipping_address"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="cartapp_shipping_addresses",
    )
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return string representation of the shipping address."""
        return f"{self.full_name}'s address for {self.order.order_number}"
