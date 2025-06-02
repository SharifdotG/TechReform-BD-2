"""Django models for the CompareApp product comparison functionality.

This module defines the database models for the product comparison system
of the TechReform e-commerce application. It enables users to compare
products across different categories side-by-side to make informed
purchasing decisions.

The comparison system supports:
- Session-based comparison for anonymous users
- User account integration for registered customers
- Multi-category product comparison via dynamic model mapping
- Unlimited products per comparison list
- Cross-category product comparisons

Models:
- CompareList: Container for a user's comparison items
- CompareItem: Individual products within a comparison list

The system uses UUID primary keys and supports dynamic product retrieval
from all ProductsApp models for comprehensive product comparison capabilities.
"""

from django.db import models
import uuid
from django.contrib.auth.models import User


class CompareList(models.Model):
    """Container model for a user's product comparison list.

    Manages a collection of products that a user wants to compare.
    Supports both authenticated users through user account linking
    and anonymous users through session-based identification.

    Attributes:
        id (UUIDField): Unique identifier for the comparison list
        user (OneToOneField): Optional link to authenticated user account
        session_id (CharField): Session identifier for anonymous users
        created_at (DateTimeField): List creation timestamp
        updated_at (DateTimeField): Last modification timestamp

    Related Models:
        - CompareItem: Individual products within this comparison list
        - User: List owner (optional for anonymous users)

    Business Rules:
        - Each authenticated user can have only one comparison list
        - Anonymous users are tracked by session ID
        - Lists are automatically created when first product is added

    Usage:
        # For authenticated users
        compare_list = CompareList.objects.get(user=request.user)

        # For anonymous users
        compare_list = CompareList.objects.get(session_id=session_key)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Compare List"
        verbose_name_plural = "Compare Lists"

    def __str__(self):
        """Return string representation of the comparison list."""
        if self.user:
            return f"Compare List for {self.user.username}"
        return f"Compare List for Guest ({self.session_id})"

    @property
    def get_compare_items_count(self):
        """Get the total number of items in the comparison list.

        Returns:
            int: Number of products currently in the comparison list

        Example:
            >>> compare_list = CompareList.objects.get(user=user)
            >>> compare_list.get_compare_items_count
            3
        """
        return self.compareitem_set.count()


class CompareItem(models.Model):
    """Individual product item within a comparison list.

    Represents a specific product added to a user's comparison list.
    Uses dynamic model mapping to support products from all categories
    available in the ProductsApp. Maintains both direct relationships
    and session-based tracking for comprehensive comparison functionality.

    Attributes:
        compare_list (ForeignKey): Reference to the parent comparison list
        session_key (CharField): Session key for anonymous user tracking
        user (ForeignKey): Optional reference to authenticated user
        product_id (CharField): UUID of the product from any category model
        category (CharField): Product category name for model lookup
        date_added (DateTimeField): Timestamp when item was added

    Related Models:
        - CompareList: The comparison list containing this item
        - User: Item owner (optional for anonymous users)
        - ProductsApp models: CPU, GPU, RAM, etc. (via dynamic lookup)

    Ordering:
        Items are ordered by date_added in descending order (newest first)

    Usage:
        # Add product to comparison
        compare_item = CompareItem.objects.create(
            compare_list=compare_list,
            user=request.user,
            product_id=product.id,
            category='CPU'
        )
    """
    compare_list = models.ForeignKey(
        CompareList, on_delete=models.CASCADE, null=True, blank=True
    )
    session_key = models.CharField(max_length=40, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product_id = models.CharField(
        max_length=255
    )  # Changed from IntegerField to CharField to accept UUID strings
    category = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_added"]

    def __str__(self):
        """Return string representation of the comparison item."""
        return f"{self.category} (ID: {self.product_id})"

    def get_product(self):
        """Retrieve the actual product object from the appropriate model.

        Uses dynamic model mapping to fetch the product instance from
        the correct ProductsApp model based on the category field.
        Supports all product categories available in the system.

        Returns:
            Model instance or None: The product object if found, None if
                                   category is invalid or product doesn't exist

        Supported Categories:
            CPU, GPU, RAM, SSD, HDD, Motherboard, Power Supply, Casing,
            Cooler, Monitor, Keyboard, Mouse, Headphone

        Error Handling:
            - Returns None for invalid categories
            - Returns None if product with given ID doesn't exist
            - Handles model import and lookup exceptions gracefully

        Example:
            >>> item = CompareItem.objects.get(id='some-uuid')
            >>> item.category = 'CPU'
            >>> product = item.get_product()
            >>> print(product.name)
            'Intel Core i7-12700K'
        """
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
