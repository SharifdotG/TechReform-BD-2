"""Views for the CompareApp module.

This module provides views for managing product comparisons in the TechReform-BD
e-commerce platform. It allows users to add, remove, and compare up to 4 products
side-by-side with detailed specifications.

Key Features:
    - Add/remove products from comparison list
    - Support for both authenticated and anonymous users
    - Category-specific specification comparisons
    - AJAX support for dynamic interactions
    - Session-based comparison lists for anonymous users
    - User-based comparison lists for authenticated users

Supported Product Categories:
    CPU, GPU, RAM, SSD, HDD, Motherboard, PowerSupply, Casing, Cooler,
    Monitor, Keyboard, Mouse, Headphone

Author: TechReform-BD Development Team
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import CompareList, CompareItem
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


def get_product_by_id_and_category(product_id, category):
    """Retrieve a product instance based on its ID and category.

    This helper function maps product categories to their corresponding
    Django model classes and retrieves the specific product instance.

    Args:
        product_id (int): The unique identifier of the product.
        category (str): The category/type of the product (e.g., 'CPU', 'GPU', etc.).

    Returns:
        Model instance or None: The product instance if found and category is valid,
        None if the category is not recognized.

    Raises:
        Http404: If the product with the given ID doesn't exist in the specified category.
    """
    if category == "CPU":
        return get_object_or_404(CPU, id=product_id)
    elif category == "GPU":
        return get_object_or_404(GPU, id=product_id)
    elif category == "RAM":
        return get_object_or_404(RAM, id=product_id)
    elif category == "SSD":
        return get_object_or_404(SSD, id=product_id)
    elif category == "HDD":
        return get_object_or_404(HDD, id=product_id)
    elif category == "Power Supply":
        return get_object_or_404(PowerSupply, id=product_id)
    elif category == "Casing":
        return get_object_or_404(Casing, id=product_id)
    elif category == "Cooler":
        return get_object_or_404(Cooler, id=product_id)
    elif category == "Monitor":
        return get_object_or_404(Monitor, id=product_id)
    elif category == "Motherboard":
        return get_object_or_404(Motherboard, id=product_id)
    elif category == "Keyboard":
        return get_object_or_404(Keyboard, id=product_id)
    elif category == "Mouse":
        return get_object_or_404(Mouse, id=product_id)
    elif category == "Headphone":
        return get_object_or_404(Headphone, id=product_id)
    else:
        return None


def get_compare_list(request):
    """Get or create a compare list for the current user or session.

    This helper function handles both authenticated and anonymous users by
    creating or retrieving their compare list. For authenticated users,
    the list is associated with their user account. For anonymous users,
    it's associated with their session.

    Args:
        request (HttpRequest): The Django request object containing user and session information.

    Returns:
        CompareList: The user's or session's compare list instance.
    """
    if request.user.is_authenticated:
        try:
            compare_list = CompareList.objects.get(user=request.user)
        except CompareList.DoesNotExist:
            compare_list = CompareList.objects.create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_id = request.session.session_key
        try:
            compare_list = CompareList.objects.get(session_id=session_id)
        except CompareList.DoesNotExist:
            compare_list = CompareList.objects.create(session_id=session_id)

    return compare_list


@require_POST
def add_to_compare(request):
    """Add a product to the user's compare list.

    This view handles adding products to the comparison list with proper validation.
    It supports both AJAX and regular form submissions, enforces a maximum of 4 items
    per compare list, and prevents duplicate additions.

    Args:
        request (HttpRequest): POST request containing product_id and product_category.

    Returns:
        JsonResponse: If AJAX request, returns JSON with status, message, and compare count.
        HttpResponse: If regular request, redirects to appropriate page with flash messages.

    Raises:
        Exception: Catches and handles any unexpected errors during the process.

    POST Parameters:
        product_id (str): The ID of the product to add to comparison.
        product_category (str): The category of the product (e.g., 'CPU', 'GPU').
    """
    try:
        product_id = request.POST.get("product_id")
        product_category = request.POST.get("product_category")

        if not product_id or not product_category:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "Product ID and category are required",
                    },
                    status=400,
                )
            messages.error(request, "Product ID and category are required")
            return redirect("product-list")

        # Get or create the compare list for the current user/session
        compare_list = get_compare_list(request)

        # Check if this product is already in the compare list
        existing_item = CompareItem.objects.filter(
            compare_list=compare_list, product_id=product_id, category=product_category
        ).first()

        if existing_item:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse(
                    {
                        "status": "info",
                        "message": "This product is already in your compare list",
                        "compare_count": compare_list.get_compare_items_count,
                    }
                )
            messages.info(request, "This product is already in your compare list")
            return redirect("view_compare_list")

        # Check if we already have 4 items in the compare list
        if CompareItem.objects.filter(compare_list=compare_list).count() >= 4:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "You can compare a maximum of 4 items. Please remove an item before adding a new one.",
                        "compare_count": compare_list.get_compare_items_count,
                    }
                )
            messages.warning(
                request,
                "You can compare a maximum of 4 items. Please remove an item before adding a new one.",
            )
            return redirect("view_compare_list")

        # Add the item to the compare list
        compare_item = CompareItem(
            compare_list=compare_list, product_id=product_id, category=product_category
        )

        # If user is authenticated, associate the item with the user as well
        if request.user.is_authenticated:
            compare_item.user = request.user

        compare_item.save()

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse(
                {
                    "status": "success",
                    "message": "Product added to your compare list",
                    "compare_count": compare_list.get_compare_items_count,
                }
            )

        messages.success(request, "Product added to your compare list")
        return redirect("view_compare_list")

    except Exception as e:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse(
                {
                    "status": "error",
                    "message": f"An error occurred: {str(e)}",
                },
                status=500,
            )
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect("product-list")


@require_POST
def remove_from_compare(request):
    """Remove a specific product from the user's compare list.

    This view handles the removal of individual items from the compare list.
    It includes permission checks to ensure users can only remove items
    they have added (for authenticated users).

    Args:
        request (HttpRequest): POST request containing the item_id to remove.

    Returns:
        HttpResponse: Redirects to the compare list view with appropriate flash messages.

    POST Parameters:
        item_id (str): The ID of the CompareItem to remove from the list.

    Security:
        - Validates that authenticated users can only remove their own items
        - Handles both authenticated and anonymous user scenarios
    """
    if request.method == "POST":
        item_id = request.POST.get("item_id")

        if not item_id:
            messages.error(request, "Item ID is required")
            return redirect("view_compare_list")

        # Get the compare item
        compare_item = get_object_or_404(CompareItem, id=item_id)

        # Check if the user has permission to delete this item
        if (
            request.user.is_authenticated
            and compare_item.user
            and compare_item.user != request.user
        ):
            messages.error(request, "You do not have permission to remove this item")
            return redirect("view_compare_list")

        # Delete the item
        compare_item.delete()

        messages.success(request, "Product removed from your compare list")
        return redirect("view_compare_list")

    return redirect("view_compare_list")


@require_POST
def clear_compare_list(request):
    """Clear all products from the user's compare list.

    This view removes all items from the user's compare list in a single operation.
    It handles both authenticated users (by user account) and anonymous users
    (by session ID).

    Args:
        request (HttpRequest): POST request to clear the compare list.

    Returns:
        HttpResponse: Redirects to the compare list view with a success message.

    Note:
        - For authenticated users: Finds compare list by user account
        - For anonymous users: Finds compare list by session ID
        - If no session exists for anonymous users, redirects without action
    """
    if request.method == "POST":
        # Get the compare list for the current user/session
        if request.user.is_authenticated:
            compare_list = CompareList.objects.filter(user=request.user).first()
        else:
            session_key = request.session.session_key
            if not session_key:
                return redirect("view_compare_list")
            compare_list = CompareList.objects.filter(session_id=session_key).first()

        if compare_list:
            # Delete all items in the compare list
            CompareItem.objects.filter(compare_list=compare_list).delete()

            messages.success(request, "Your compare list has been cleared")

        return redirect("view_compare_list")

    return redirect("view_compare_list")


def view_compare_list(request):
    """Display the product comparison page with detailed specifications.

    This view renders the comparison page showing all products in the user's
    compare list. It dynamically determines product specifications based on
    categories and provides different comparison views for same-category vs
    mixed-category comparisons.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered comparison page with product details and specifications.

    Template Context:
        products (list): List of product objects in the compare list.
        same_category (bool): Whether all products belong to the same category.
        category (str): The product category if all products are the same type.
        category_specs (dict): Category-specific specifications for comparison.
        common_specs (dict): Common specifications available for all products.

    Features:
        - Handles both authenticated and anonymous users
        - Creates sessions for anonymous users if needed
        - Dynamically loads category-specific specifications
        - Supports comparison of up to 4 products
        - Provides detailed spec comparisons for same-category products
        - Fallback to basic comparison for mixed-category products
    """
    # Get the compare list for the current user/session
    if request.user.is_authenticated:
        compare_list, created = CompareList.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        compare_list, created = CompareList.objects.get_or_create(
            session_id=session_key
        )

    # Get all items in the compare list
    compare_items = CompareItem.objects.filter(compare_list=compare_list)

    products = []
    same_category = True
    current_category = None
    category_specs = {}  # Dictionary to store category-specific specifications
    common_specs = {
        "brand": "Brand",
        "model": "Model",
        "warranty": "Warranty",
        "price": "Price",
        "regular_price": "Regular Price",
        "discount_percentage": "Discount Percentage",
    }  # Common specs for all products

    # Process the items to get the actual product objects
    for item in compare_items:
        product = item.get_product()
        if product:
            # Add the compare item ID to the product for later reference
            product.compare_item_id = item.id
            products.append(product)

            # Check if all products are of the same category
            if current_category is None:
                current_category = item.category
            elif current_category != item.category:
                same_category = False

    # If products are of same category, get all relevant specs for that category
    if same_category and products:
        if current_category == "CPU":
            category_specs = {
                "socket": "Socket",
                "cores": "Cores",
                "threads": "Threads",
                "base_frequency": "Base Frequency",
                "boost_frequency": "Boost Frequency",
                "cache": "Cache",
                "tdp": "TDP",
                "processor_graphics": "Integrated Graphics",
            }
        elif current_category == "GPU":
            category_specs = {
                "vram_capacity": "Memory Capacity",
                "memory_type": "Memory Type",
                "memory_bus": "Memory Bus",
                "core_clock": "Core Clock",
                "memory_clock": "Memory Clock",
                "cores": "CUDA Cores",
                "core_type": "Core Type",
                "memory_interface": "Interface",
                "dp_ports": "DisplayPorts",
                "hdmi_ports": "HDMI Ports",
            }
        elif current_category == "RAM":
            category_specs = {
                "memory_capacity": "Capacity",
                "ram_type": "Type",
                "frequency": "Frequency",
                "ram_class": "Class",
                "cas_latency": "CAS Latency",
                "heat_spreader": "Heat Spreader",
                "rgb": "RGB Lighting",
            }
        elif current_category == "Power Supply":
            category_specs = {
                "wattage": "Wattage",
                "efficiency": "Efficiency",
                "modularity": "Modularity",
                "form_factor": "Form Factor",
                "fan_size": "Fan Size",
                "pcie_connectors": "PCIe Connectors",
                "sata_connectors": "SATA Connectors",
            }
        elif current_category == "Casing":
            category_specs = {
                "form_factor": "Form Factor",
                "side_panel": "Side Panel",
                "pre_installed_fans": "Pre-installed Fans",
                "ssd_bays": "SSD Bays",
                "hdd_bays": "HDD Bays",
                "expansion_slots": "Expansion Slots",
                "rgb": "RGB Lighting",
                "dust_filters": "Dust Filters",
                "cable_management": "Cable Management",
                "power_supply": "Included Power Supply",
            }
        elif current_category == "Monitor":
            category_specs = {
                "screen_size": "Screen Size",
                "screen_resolution": "Resolution",
                "refresh_rate": "Refresh Rate",
                "aspect_ratio": "Aspect Ratio",
                "response_time": "Response Time",
                "panel_type": "Panel Type",
                "brightness": "Brightness",
                "hdmi_ports": "HDMI Ports",
                "dp_ports": "DisplayPorts",
                "vga_ports": "VGA Ports",
                "dvi_ports": "DVI Ports",
                "speakers": "Built-in Speakers",
            }
        elif current_category == "SSD" or current_category == "HDD":
            category_specs = {
                "storage_capacity": "Capacity",
                "form_factor": "Form Factor",
                "interface": "Interface",
                "read_speed": "Read Speed",
                "write_speed": "Write Speed",
                "cache": "Cache",
                "rpm": "Rotation Speed",  # Mainly for HDDs
            }
        elif current_category == "Motherboard":
            category_specs = {
                "socket": "Socket",
                "chipset": "Chipset",
                "form_factor": "Form Factor",
                "memory_slots": "Memory Slots",
                "memory_type": "Memory Type",
                "max_memory": "Maximum Memory",
                "pcie_slots": "PCIe Slots",
                "m2_slots": "M.2 Slots",
                "sata_ports": "SATA Ports",
                "usb_ports": "USB Ports",
                "wifi_bluetooth": "Wi-Fi & Bluetooth",
            }
        elif current_category == "Keyboard":
            category_specs = {
                "key_type": "Key Type",
                "keyboard_size": "Size",
                "switch_type": "Switch Type",
                "number_of_keys": "Number of Keys",
                "interface": "Interface",
                "rgb": "RGB Lighting",
                "cable_length": "Cable Length",
            }
        elif current_category == "Mouse":
            category_specs = {
                "mouse_type": "Mouse Type",
                "use_type": "Usage Type",
                "number_of_buttons": "Number of Buttons",
                "max_dpi": "Max DPI",
                "interface": "Interface",
                "rgb": "RGB Lighting",
                "cable_length": "Cable Length",
            }
        elif current_category == "Cooler":
            category_specs = {
                "cooler_type": "Type",
                "cooler_size": "Size",
                "fan_speed": "Fan Speed",
                "noise_level": "Noise Level",
                "rgb": "RGB Lighting",
                "tdp": "TDP Rating",
            }
        elif current_category == "Headphone":
            category_specs = {
                "headphone_type": "Type",
                "connection": "Connection",
                "frequency_response": "Frequency Response",
                "impedance": "Impedance",
                "sensitivity": "Sensitivity",
                "input_jack": "Input Jack",
                "cable_length": "Cable Length",
                "microphone": "Microphone",
                "noise_cancellation": "Noise Cancellation",
                "rgb": "RGB Lighting",
            }

    context = {
        "products": products,
        "same_category": same_category,
        "category": current_category,
        "category_specs": category_specs,  # Pass category-specific specs to template
        "common_specs": common_specs,  # Pass common specs to template
    }

    return render(request, "compare/compare.html", context)
