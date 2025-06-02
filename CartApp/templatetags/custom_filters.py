"""Django template filters and tags for cart functionality.

This module provides custom template filters and tags specifically designed for
enhancing the shopping cart and e-commerce functionality in the TechReform
application. It includes utilities for currency formatting, discount calculations,
mathematical operations, and dynamic product image retrieval.

The filters are designed to work seamlessly with Django's template system and
provide consistent formatting and calculations across all cart-related templates.
All filters include proper error handling to prevent template rendering failures.

Available Filters:
- currency: Format numeric values as currency with custom symbols
- discount_percent: Calculate and display discount percentages
- multiply: Perform multiplication operations in templates
- sub: Perform subtraction operations in templates

Available Tags:
- get_product_image: Dynamically retrieve product images based on category

All filters handle edge cases and invalid inputs gracefully to ensure robust
template rendering even with malformed data.
"""

from django import template
from django.template.defaultfilters import floatformat
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()


@register.filter(name="currency")
def currency(value, currency_symbol="৳"):
    """Format numeric values as currency with proper formatting.

    Converts numeric values to currency format with thousands separators
    and the specified currency symbol. Uses Django's built-in formatting
    functions for consistent number formatting.

    Args:
        value (float|int|str|None): The numeric value to format as currency
        currency_symbol (str): The currency symbol to prepend (default: "৳")

    Returns:
        str: Formatted currency string with symbol and thousands separators
             Returns empty string if value is None

    Examples:
        Template usage:
        {{ 1500|currency }} -> "৳1,500"
        {{ 1500.50|currency:"$" }} -> "$1,501"
        {{ product.price|currency }} -> "৳12,500"

    Note:
        Uses floatformat with 0 decimal places for whole number display
        and intcomma for thousands separator formatting.
    """
    if value is None:
        return ""

    formatted = floatformat(value, 0)
    formatted = intcomma(formatted)
    return f"{currency_symbol}{formatted}"


@register.filter(name="discount_percent")
def discount_percent(price, regular_price):
    """Calculate and format discount percentage between two prices.

    Computes the percentage discount from regular price to sale price
    and returns it as a formatted percentage string. Handles edge cases
    like zero or invalid prices gracefully.

    Args:
        price (float|int|str): The discounted/sale price
        regular_price (float|int|str): The original/regular price

    Returns:
        str: Formatted percentage string (e.g., "25%")
             Returns "0%" for invalid inputs or no discount

    Examples:
        Template usage:
        {{ 75|discount_percent:100 }} -> "25%"
        {{ product.sale_price|discount_percent:product.regular_price }} -> "15%"
        {{ 100|discount_percent:100 }} -> "0%"

    Calculation:
        discount_percent = ((regular_price - price) / regular_price) * 100

    Error Handling:
        Returns "0%" if:
        - Either price is None, zero, or negative
        - Values cannot be converted to float
        - Regular price is less than or equal to zero
    """
    if not price or not regular_price or float(regular_price) <= 0:
        return "0%"

    discount = ((float(regular_price) - float(price)) / float(regular_price)) * 100
    return f"{int(discount)}%"


@register.filter(name="multiply")
def multiply(value, arg):
    """Perform multiplication operation in templates.

    Multiplies two numeric values together, useful for calculating totals,
    subtotals, and other mathematical operations within templates without
    requiring view-level calculations.

    Args:
        value (float|int|str): The first numeric value (multiplicand)
        arg (float|int|str): The second numeric value (multiplier)

    Returns:
        float: The product of value and arg
               Returns 0 if either value cannot be converted to float

    Examples:
        Template usage:
        {{ quantity|multiply:price }} -> Calculate line total
        {{ 5|multiply:10 }} -> 50.0
        {{ item.quantity|multiply:item.unit_price }} -> Line item total

    Error Handling:
        Returns 0 if:
        - Either value is None
        - Values cannot be converted to float (ValueError)
        - Values are of incompatible types (TypeError)

    Note:
        Useful for cart calculations where quantity × price = line total
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter(name="sub")
def sub(value, arg):
    """Perform subtraction operation in templates.

    Subtracts the second value from the first value, useful for calculating
    discounts, remaining amounts, and other mathematical operations within
    templates without requiring view-level calculations.

    Args:
        value (float|int|str): The minuend (value to subtract from)
        arg (float|int|str): The subtrahend (value to subtract)

    Returns:
        float: The difference of value minus arg
               Returns 0 if either value cannot be converted to float

    Examples:
        Template usage:
        {{ total|sub:discount }} -> Calculate final total after discount
        {{ 100|sub:25 }} -> 75.0
        {{ cart.total|sub:cart.shipping_cost }} -> Net total

    Error Handling:
        Returns 0 if:
        - Either value is None
        - Values cannot be converted to float (ValueError)
        - Values are of incompatible types (TypeError)

    Note:
        Useful for discount calculations and price adjustments in templates
    """
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return 0


@register.simple_tag
def get_product_image(product_category, product_id):
    """Dynamically retrieve product image URL based on category and ID.

    This template tag provides a unified interface for accessing product images
    across different product category models. It maps product categories to their
    corresponding model classes and retrieves the first available image for display.

    Args:
        product_category (str): The category name of the product (e.g., "CPU", "GPU")
        product_id (int|str): The unique identifier of the product

    Returns:
        str|None: The URL of the first available product image
                 Returns None if no image is found or product doesn't exist

    Usage:
        Template tag usage:
        {% get_product_image item.product_category item.product_id as product_image %}
        {% if product_image %}
            <img src="{{ product_image }}" alt="Product Image">
        {% endif %}

    Supported Categories:
        - CPU, GPU, Motherboard, RAM, SSD, HDD
        - Power Supply, Casing, Cooler
        - Monitor, Keyboard, Mouse, Headphone

    Image Priority:
        Returns the first available image in this order:
        1. image1 field
        2. image2 field
        3. image3 field

    Error Handling:
        Returns None for:
        - Unknown/unsupported product categories
        - Non-existent product IDs
        - Products without any images
        - Import errors or database connection issues
        - Invalid data types

    Note:
        This tag dynamically imports ProductsApp models to avoid circular imports
        and provides a flexible interface for the cart system to display product
        images without tight coupling to specific product models.
    """
    from django.core.exceptions import ObjectDoesNotExist

    try:
        # Map product categories to their respective model
        from ProductsApp.models import (
            CPU,
            GPU,
            Motherboard,
            RAM,
            SSD,
            HDD,
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
            "Motherboard": Motherboard,
            "RAM": RAM,
            "SSD": SSD,
            "HDD": HDD,
            "Power Supply": PowerSupply,
            "Casing": Casing,
            "Cooler": Cooler,
            "Monitor": Monitor,
            "Keyboard": Keyboard,
            "Mouse": Mouse,
            "Headphone": Headphone,
        }

        # Get the appropriate model based on category
        model = category_model_map.get(product_category)
        if not model:
            return None

        # Try to get the product
        product = model.objects.get(id=product_id)

        # Return the first available image
        if hasattr(product, "image1") and product.image1:
            return product.image1.url
        elif hasattr(product, "image2") and product.image2:
            return product.image2.url
        elif hasattr(product, "image3") and product.image3:
            return product.image3.url

        return None

    except (ImportError, ObjectDoesNotExist, AttributeError, ValueError):
        return None
