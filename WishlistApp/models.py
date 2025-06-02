"""
Django models for WishlistApp.

This module defines the database models for the wishlist functionality
in the TechReform e-commerce application. It provides models for managing
user wishlists and individual wishlist items, supporting both authenticated
and anonymous users through session-based storage.

Models:
    WishList: Represents a user's wishlist container
    WishlistItem: Represents individual products in a wishlist

Key Features:
    - Support for authenticated and anonymous users
    - UUID-based primary keys for enhanced security
    - Relationship with all product categories
    - Automatic timestamp tracking
    - Session-based wishlist management
"""

from django.db import models
import uuid
from django.contrib.auth.models import User
from ProductsApp.models import (
    CPU,
    GPU,
    RAM,
    SSD,
    HDD,
    Motherboard,
    PowerSupply,
    Casing,
    Cooler,
    Monitor,
    Keyboard,
    Mouse,
    Headphone,
)


class WishList(models.Model):
    """
    Model representing a user's wishlist container.

    This model serves as the main container for a user's wishlist items.
    It supports both authenticated users (linked via User model) and
    anonymous users (linked via session ID). Each user or session can
    have only one wishlist.

    Attributes:
        id (UUIDField): Primary key using UUID4 for enhanced security
            and to prevent enumeration attacks.
        user (OneToOneField): Optional relationship to Django User model
            for authenticated users.
        session_id (CharField): Optional session identifier for anonymous
            users' wishlists.
        created_at (DateTimeField): Timestamp when the wishlist was created.
        updated_at (DateTimeField): Timestamp when the wishlist was last modified.

    Methods:
        __str__: Returns a human-readable string representation.
        get_wishlist_items_count: Property that returns the count of items
            in the wishlist.

    Meta:
        verbose_name: Human-readable name for the model.
        verbose_name_plural: Human-readable plural name for the model.

    Note:
        Either 'user' or 'session_id' should be set, but not both.
        The model uses a OneToOne relationship with User to ensure
        each user has only one wishlist.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Wish List"
        verbose_name_plural = "Wish Lists"

    def __str__(self):
        if self.user:
            return f"Wish List for {self.user.username}"
        return f"Wish List for Guest ({self.session_id})"

    @property
    def get_wishlist_items_count(self):
        return self.wishlistitem_set.count()


class WishlistItem(models.Model):
    """
    Model representing individual items in a user's wishlist.

    This model stores references to products that users have added to their
    wishlists. It supports products from multiple categories and maintains
    relationships with both the parent WishList and the User for authenticated
    users. The model uses generic relationships to handle different product
    types through category and product_id fields.

    Attributes:
        wishlist (ForeignKey): Reference to the parent WishList object.
            Can be null for backward compatibility.
        session_key (CharField): Session identifier for anonymous users.
            Used for legacy support and session-based item tracking.
        user (ForeignKey): Reference to the User who added the item.
            Set for authenticated users to enable user-specific operations.
        product_id (CharField): String representation of the product's UUID.
            Stored as CharField to handle UUID strings from different models.
        category (CharField): The product category (e.g., 'CPU', 'GPU').
            Used to determine which model to query for product details.
        date_added (DateTimeField): Timestamp when the item was added to
            the wishlist.

    Methods:
        __str__: Returns a human-readable string representation showing
            category and product ID.
        get_product: Retrieves the actual product object based on category
            and product_id. Returns None if product doesn't exist.

    Meta:
        ordering: Items are ordered by date_added in descending order
            (newest first).

    Supported Product Categories:
        CPU, GPU, RAM, SSD, HDD, Motherboard, Power Supply, Casing,
        Cooler, Monitor, Keyboard, Mouse, Headphone

    Note:
        The product_id field stores UUID strings rather than direct foreign
        keys to maintain flexibility across different product models.
    """

    wishlist = models.ForeignKey(
        WishList, on_delete=models.CASCADE, null=True, blank=True
    )
    session_key = models.CharField(max_length=40, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product_id = models.CharField(
        max_length=255
    )  # Using CharField to accept UUID strings
    category = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_added"]

    def __str__(self):
        return f"{self.category} (ID: {self.product_id})"

    def get_product(self):
        """
        Retrieve the actual product object based on category and product_id.

        This method maps the category string to the appropriate Django model
        class and attempts to retrieve the product instance using the stored
        product_id. It provides a unified interface for accessing products
        across different categories.

        Returns:
            Model instance or None: The product object if found and exists,
            None if the category is not recognized or if the product with
            the given ID doesn't exist in the database.

        Example:
            >>> item = WishlistItem.objects.get(id=1)
            >>> product = item.get_product()
            >>> if product:
            ...     print(f"Product name: {product.name}")
            ... else:
            ...     print("Product not found")

        Note:
            This method performs a database query each time it's called.
            Consider caching or prefetching if called multiple times for
            the same item in a single request.

        Raises:
            No exceptions are raised. Returns None for any errors to
            maintain consistency and prevent crashes from missing products.
        """
        category_model_map = {
            "CPU": CPU,
            "GPU": GPU,
            "RAM": RAM,
            "SSD": SSD,
            "HDD": HDD,
            "Motherboard": Motherboard,
            "Power Supply": PowerSupply,
            "Casing": Casing,
            "Cooler": Cooler,
            "Monitor": Monitor,
            "Keyboard": Keyboard,
            "Mouse": Mouse,
            "Headphone": Headphone,
        }

        model_class = category_model_map.get(self.category)
        if not model_class:
            return None

        try:
            return model_class.objects.get(id=self.product_id)
        except model_class.DoesNotExist:
            return None
