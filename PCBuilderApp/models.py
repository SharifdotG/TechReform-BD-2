"""PC Builder application models.

This module contains Django models for managing PC build configurations,
including PC builds and their associated components. Users can create
builds with various hardware components and track their total cost,
power requirements, and completeness status.
"""

from django.db import models
import uuid
from django.contrib.auth.models import User
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


class PCBuilder(models.Model):
    """PC build configuration model.

    Represents a PC build configuration created by a user or anonymous session.
    Each build can contain multiple components and tracks information like
    total cost, power requirements, and completeness status.

    Attributes:
        id (UUIDField): Primary key using UUID4 for uniqueness.
        user (ForeignKey): Associated user who created the build (optional for anonymous users).
        name (CharField): Custom name for the build configuration.
        is_public (BooleanField): Whether the build is visible to other users.
        created_at (DateTimeField): Timestamp when the build was created.
        updated_at (DateTimeField): Timestamp when the build was last modified.
        session_id (CharField): Session identifier for anonymous users.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="pcbuilderapp_builds",
    )
    name = models.CharField(
        max_length=100, blank=True, null=True, help_text="Name of the configuration"
    )
    is_public = models.BooleanField(
        default=False, help_text="Make this build visible to other users"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    session_id = models.CharField(
        max_length=255, blank=True, null=True, help_text="For non-logged in users"
    )

    def __str__(self):
        """Return string representation of the PC build.

        Returns:
            str: Build name if available, otherwise build ID.
        """
        return f"PC Build {self.name or self.id}"

    @property
    def get_total_price(self):
        """Calculate total price of all components in the build.

        Sums up the prices of all components that have been selected
        for this PC build configuration.

        Returns:
            decimal.Decimal: Total price of all components, or 0 if no components.
        """
        items = self.pcbuilderitem_set.all()
        total = sum(item.product_price for item in items if item.product_id)
        return total

    @property
    def get_item_count(self):
        """Get count of components with products assigned.

        Counts only the components that have actual products selected,
        not empty component slots.

        Returns:
            int: Number of components with products assigned.
        """
        items = self.pcbuilderitem_set.all()
        return sum(1 for item in items if item.product_id)

    @property
    def get_recommended_wattage(self):
        """Calculate recommended power supply wattage.

        Calculates the total TDP (Thermal Design Power) of all components
        and adds 100W buffer for safety and future upgrades.

        Returns:
            int: Recommended wattage (total TDP + 100W), or 0 if no components.
        """
        items = self.pcbuilderitem_set.all()
        total_tdp = sum(item.product_tdp or 0 for item in items if item.product_id)
        return total_tdp + 100 if total_tdp > 0 else 0

    @property
    def is_complete(self):
        """Check if all essential components are selected.

        Verifies that the build contains all the essential components
        needed for a functional PC: CPU, Motherboard, RAM, and Power Supply.

        Returns:
            bool: True if all essential components are present, False otherwise.
        """
        essential_categories = ["CPU", "Motherboard", "RAM", "Power Supply"]
        return all(
            self.pcbuilderitem_set.filter(component_type=category).exists()
            and self.pcbuilderitem_set.get(component_type=category).product_id
            is not None
            for category in essential_categories
        )


class PCBuilderItem(models.Model):
    """Individual component item within a PC build.

    Represents a single component slot in a PC build configuration.
    Each item corresponds to a specific component type (CPU, GPU, etc.)
    and can have a product assigned to it along with cached product information.

    Attributes:
        COMPONENT_CHOICES (list): Available component types for PC builds.
        id (UUIDField): Primary key using UUID4 for uniqueness.
        pc_builder (ForeignKey): Reference to the parent PC build.
        component_type (CharField): Type of component (CPU, GPU, etc.).
        product_id (UUIDField): UUID of the selected product (optional).
        product_name (CharField): Cached name of the selected product.
        product_price (DecimalField): Cached price of the selected product.
        product_tdp (IntegerField): Cached TDP value of the selected product.
    """
    COMPONENT_CHOICES = [
        ("CPU", "CPU"),
        ("Cooler", "CPU Cooler"),
        ("Motherboard", "Motherboard"),
        ("RAM", "Memory"),
        ("SSD", "SSD"),
        ("HDD", "HDD"),
        ("GPU", "Graphics Card"),
        ("Power Supply", "Power Supply"),
        ("Casing", "Case"),
        ("Monitor", "Monitor"),
        ("Keyboard", "Keyboard"),
        ("Mouse", "Mouse"),
        ("Headphone", "Headphone"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pc_builder = models.ForeignKey(PCBuilder, on_delete=models.CASCADE)
    component_type = models.CharField(max_length=50, choices=COMPONENT_CHOICES)
    product_id = models.UUIDField(null=True, blank=True)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    product_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    product_tdp = models.IntegerField(
        null=True, blank=True, help_text="Component TDP in watts"
    )

    def __str__(self):
        """Return string representation of the PC builder item.

        Returns:
            str: Component type and associated PC build ID.
        """
        return f"{self.component_type} for {self.pc_builder.id}"

    def get_product(self):
        """Get the actual product instance from the ProductsApp.

        Retrieves the full product object based on the component type
        and product ID. Handles different product models and provides
        error handling for missing products.

        Returns:
            Model instance or None: The product object if found, None if not found
                                   or if no product_id is set.

        Raises:
            None: Exceptions are caught and logged, method returns None on error.
        """
        if not self.product_id:
            return None

        # Map component types to model classes
        model_dict = {
            "CPU": CPU,
            "Cooler": Cooler,
            "Motherboard": Motherboard,
            "RAM": RAM,
            "SSD": SSD,
            "HDD": HDD,
            "GPU": GPU,
            "Power Supply": PowerSupply,
            "PowerSupply": PowerSupply,  # Alias for consistency
            "Casing": Casing,
            "Monitor": Monitor,
            "Keyboard": Keyboard,
            "Mouse": Mouse,
            "Headphone": Headphone,
        }

        if self.component_type in model_dict:
            model = model_dict[self.component_type]
            try:
                return model.objects.get(id=self.product_id)
            except model.DoesNotExist:
                print(
                    f"Product not found for component type {self.component_type} with ID {self.product_id}"
                )
                return None

        print(f"Unknown component type: {self.component_type}")
        return None

    class Meta:
        """Meta configuration for PCBuilderItem model.

        Ensures that each PC build can only have one item per component type,
        preventing duplicate components in a single build.
        """
        unique_together = ("pc_builder", "component_type")
