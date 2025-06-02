"""Django template tags and filters for product-related functionality.

This module provides custom template tags and filters specifically designed
for handling product data in Django templates. It includes utilities for
dynamic image access, attribute retrieval, and dictionary operations.

The filters in this module are designed to work with product models and
provide enhanced functionality for template rendering in the TechReform
e-commerce application.
"""

from django import template

register = template.Library()


@register.filter
def get_dynamic_image(product, i):
    """Retrieve a dynamically named image field from a product object.

    This filter allows templates to access image fields with numeric suffixes
    (e.g., image1, image2, image3) using a dynamic approach. This is particularly
    useful when displaying multiple product images in templates without
    hardcoding field names.

    Args:
        product: The product model instance containing image fields.
        i (int or str): The numeric suffix for the image field name. Will be
            converted to string and appended to 'image' to form the field name.

    Returns:
        ImageField or None: The image field if it exists and has a value,
        None if the field doesn't exist, has no value, or if an error occurs.

    Usage:
        In templates: {{ product|get_dynamic_image:1 }}
        This will attempt to access product.image1

    Example:
        {% for i in "123"|make_list %}
            {% with image=product|get_dynamic_image:i %}
                {% if image %}
                    <img src="{{ image.url }}" alt="Product image {{ i }}">
                {% endif %}
            {% endwith %}
        {% endfor %}

    Note:
        Returns None gracefully if the attribute doesn't exist or if any
        AttributeError or ValueError occurs during access.
    """
    try:
        field_name = f"image{i}"
        image_field = getattr(product, field_name, None)
        return image_field if image_field else None
    except (AttributeError, ValueError):
        return None


@register.filter
def get_attr(obj, attr_name):
    """Dynamically retrieve an attribute from any object.

    This filter provides a generic way to access object attributes dynamically
    in Django templates. It's useful when the attribute name is stored in a
    variable or needs to be determined at runtime.

    Args:
        obj: Any Python object from which to retrieve an attribute.
        attr_name (str): The name of the attribute to retrieve from the object.

    Returns:
        Any or None: The value of the requested attribute if it exists,
        None if the attribute doesn't exist or if an error occurs during access.

    Usage:
        In templates: {{ product|get_attr:"image1" }}
        With variables: {{ product|get_attr:field_name }}

    Example:
        {% with field_name="price" %}
            {{ product|get_attr:field_name }}
        {% endwith %}

        <!-- Dynamic field access in loops -->
        {% for field in field_list %}
            {{ product|get_attr:field }}
        {% endfor %}

    Note:
        This filter safely handles cases where the attribute doesn't exist
        or is inaccessible, returning None instead of raising an exception.
        This makes it safe to use in templates without breaking rendering.
    """
    try:
        return getattr(obj, attr_name, None)
    except (AttributeError, ValueError):
        return None


@register.filter
def get_item(dictionary, key):
    """Retrieve an item from a dictionary using a dynamic key.

    This filter enables safe dictionary access in Django templates using
    dynamic keys. It provides a template-friendly way to access dictionary
    values when the key is stored in a variable or needs to be determined
    at runtime.

    Args:
        dictionary (dict): The dictionary from which to retrieve a value.
        key: The key to look up in the dictionary. Can be any hashable type
            that's valid as a dictionary key (string, int, etc.).

    Returns:
        Any: The value associated with the key if it exists in the dictionary,
        or an empty list ([]) if the key doesn't exist. The default empty list
        return value is particularly useful for template contexts where you
        might iterate over the result.

    Usage:
        In templates: {{ my_dict|get_item:my_key }}
        With string keys: {{ categories|get_item:"electronics" }}
        With variable keys: {{ data|get_item:category_name }}

    Example:
        <!-- Accessing nested data structures -->
        {% with category_items=products_by_category|get_item:current_category %}
            {% for product in category_items %}
                {{ product.name }}
            {% endfor %}
        {% endwith %}

        <!-- Safe access with fallback -->
        {% for item in user_preferences|get_item:section_name %}
            {{ item }}
        {% empty %}
            No items found for this section.
        {% endfor %}

    Note:
        Uses the dictionary's .get() method, which returns the default value
        (empty list) if the key is not found, making this filter safe to use
        without checking for key existence first.
    """
    return dictionary.get(key, [])
