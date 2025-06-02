"""
Django views for the PCBuilderApp.

This module contains all view functions for the PC Builder functionality in the
TechReform e-commerce application. It provides a comprehensive tool for users
to build custom PC configurations by selecting compatible components and tracking
total cost, power requirements, and compatibility warnings.

View Categories:
    Main PC Builder Views:
        - pc_builder: Main PC builder interface with current build display
        - add_component: Add individual components to a build
        - remove_component: Remove components from a build
        - component_selection: Component category selection interface
        - get_components: AJAX component fetching with filtering
        - save_build: Save current build configuration
        - load_build: Load existing build configuration
        - delete_build: Delete saved build configurations

    Build Management Views:
        - my_builds: User's saved build list
        - build_detail: Detailed view of a specific build
        - share_build: Share build configuration with others
        - export_build: Export build as PDF or other formats

    Compatibility Views:
        - check_compatibility: Validate component compatibility
        - get_compatibility_warnings: AJAX compatibility checking
        - component_recommendations: Suggest compatible components

Key Features:
    - Real-time compatibility checking
    - Component filtering by specifications and compatibility
    - Power consumption calculation and PSU recommendations
    - Price tracking and budget management
    - Build sharing and export functionality
    - Component availability and stock checking
    - Performance estimation and bottleneck analysis

Component Categories Supported:
    - CPU: Processor selection with socket compatibility
    - Motherboard: Board selection with CPU socket matching
    - RAM: Memory with motherboard compatibility
    - GPU: Graphics cards with power and case compatibility
    - Storage: SSD/HDD selection with interface matching
    - Power Supply: PSU with adequate wattage calculation
    - Cooling: CPU coolers with socket compatibility
    - Case: Chassis with motherboard form factor support
    - Peripherals: Monitor, keyboard, mouse, headphones

Build Validation:
    - Socket compatibility (CPU-Motherboard)
    - Power requirements (Components-PSU)
    - Physical fit (GPU length, CPU cooler height)
    - Memory compatibility (DDR type, speeds)
    - Interface compatibility (SATA, PCIe slots)

AJAX Features:
    - Real-time component filtering
    - Dynamic price updates
    - Instant compatibility checks
    - Live power consumption calculation
    - Component recommendation system

Security:
    - User authentication for build saving
    - Build ownership validation
    - Input sanitization and validation
    - CSRF protection on all forms

Dependencies:
    - ProductsApp models for component data
    - Django's AJAX framework for dynamic updates
    - PDF generation libraries for exports
    - Compatibility checking algorithms
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from django.db.models import Q
from decimal import Decimal
import json
import uuid
from .models import PCBuilder, PCBuilderItem
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
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from io import BytesIO
import os
from django.conf import settings
from datetime import datetime


def pc_builder(request):
    """
    Display the main PC Builder page with current build state and compatibility checks.

    This view renders the main PC Builder interface where users can view their current build,
    see compatibility status, power requirements, and build completion progress. It handles
    both authenticated users and anonymous sessions.

    Args:
        request (HttpRequest): The HTTP request object containing user session and data.

    Returns:
        HttpResponse: Rendered PC Builder page with build context including:
            - Current build components and their details
            - Price calculations (components, peripherals, assembly fee, total)
            - Compatibility status and any issues found
            - Power consumption analysis and PSU adequacy
            - Build completion percentage and buildable status
            - Share URL for the current build configuration

    Context Variables:
        build (dict): Dictionary mapping component types to selected products
        components_price (Decimal): Total price of core PC components
        peripherals_price (Decimal): Total price of peripherals (keyboard, mouse, headphone)
        assembly_fee (Decimal): Calculated assembly fee (5% of components price)
        total_price (Decimal): Complete build total including all fees
        is_buildable (bool): Whether build has minimum required components
        completion_percentage (int): Percentage of core components selected (0-100)
        compatibility_status (dict): Compatibility check results with status and issues
        power_status (dict): PSU adequacy status (good/warning/critical/not_selected)
        total_wattage (int): Sum of all component TDP values
        recommended_wattage (int): Recommended PSU wattage (total + 100W buffer)
        share_url (str): Absolute URL for sharing the current build
    """
    # Get or create a PC builder instance
    pc_build = get_or_create_pc_builder(request)

    # Initialize the PC builder with empty component slots if it's new
    initialize_pc_builder(pc_build)

    # Create a build object with proper structure for the template
    build = {}

    # Map component types to template attributes
    component_map = {
        "CPU": "cpu",
        "Cooler": "cpu_cooler",  # Changed from 'cooler' to 'cpu_cooler' to match template
        "Motherboard": "motherboard",
        "RAM": "ram",
        "SSD": "ssd",
        "HDD": "hdd",
        "GPU": "gpu",
        "Power Supply": "power_supply",
        "Casing": "casing",
        "Monitor": "monitor",
        "Keyboard": "keyboard",
        "Mouse": "mouse",
        "Headphone": "headphone",
    }

    # Get all components for each category
    for component_type, attr_name in component_map.items():
        builder_item = pc_build.pcbuilderitem_set.filter(
            component_type=component_type
        ).first()
        if builder_item and builder_item.product_id:
            build[attr_name] = builder_item.get_product()
        else:
            build[attr_name] = None

    # Calculate build information
    components_price = sum(
        item.product_price or 0
        for item in pc_build.pcbuilderitem_set.all()
        if item.product_id
        and item.component_type not in ["Keyboard", "Mouse", "Headphone"]
    )

    peripherals_price = sum(
        item.product_price or 0
        for item in pc_build.pcbuilderitem_set.all()
        if item.product_id and item.component_type in ["Keyboard", "Mouse", "Headphone"]
    )

    # Calculate assembly fee (example: 5% of components price)
    assembly_fee = (
        components_price * Decimal("0.05") if components_price > 0 else Decimal("0")
    )

    # Calculate total price
    total_price = components_price + peripherals_price + assembly_fee

    # Check if the build is complete enough to purchase
    is_buildable = all(
        build[attr] is not None
        for attr in ["cpu", "motherboard", "ram", "power_supply", "casing"]
    )

    # Calculate completion percentage and essential components count
    core_components = [
        "cpu",
        "cpu_cooler",
        "motherboard",
        "ram",
        "ssd",
        "hdd",
        "gpu",
        "power_supply",
        "casing",
    ]
    essential_components = [
        "cpu",
        "cpu_cooler",
        "motherboard",
        "ram",
        "ssd",
        "hdd",
        "gpu",
        "power_supply",
        "casing",
    ]

    completed_components = sum(1 for c in core_components if build[c] is not None)
    essential_components_selected = sum(
        1 for c in essential_components if build[c] is not None
    )
    completion_percentage = int((completed_components / 8) * 100)

    # Check compatibility - initialize with appropriate status based on component selection
    compatibility_issues = []
    total_wattage = 0
    recommended_wattage = 0

    # Check if any components are selected at all
    has_components = any(build[attr] is not None for attr in component_map.values())

    if not has_components:
        compatibility_status = {"status": "not_checked", "issues": []}
        power_status = {"status": "not_checked"}
    else:
        # CPU and Motherboard compatibility check
        if build["cpu"] and build["motherboard"]:
            if build["cpu"].socket != build["motherboard"].socket:
                compatibility_issues.append(
                    f"CPU socket ({build['cpu'].socket}) doesn't match motherboard socket ({build['motherboard'].socket})"
                )

        # RAM and Motherboard compatibility check
        if build["ram"] and build["motherboard"]:
            if build["ram"].ram_type != build["motherboard"].memory_type:
                compatibility_issues.append(
                    f"RAM type ({build['ram'].ram_type}) doesn't match motherboard memory type ({build['motherboard'].memory_type})"
                )

        # Case and Motherboard compatibility check
        if build["casing"] and build["motherboard"]:
            if build["motherboard"].form_factor not in build["casing"].form_factor:
                compatibility_issues.append(
                    f"Form factor mismatch: Motherboard is {build['motherboard'].form_factor} but case supports {build['casing'].form_factor}"
                )

        # Set compatibility status based on issues found
        if compatibility_issues:
            compatibility_status = {
                "status": "incompatible",
                "issues": compatibility_issues,
            }
        else:
            compatibility_status = {"status": "compatible", "issues": []}

        # Calculate total power consumption
        total_wattage = sum(
            getattr(component, "tdp", 0) or 0
            for component in build.values()
            if component is not None
        )
        # Add 100W buffer for recommended wattage
        recommended_wattage = total_wattage + 100

        # Check power supply adequacy if present
        if build["power_supply"]:
            if build["power_supply"].wattage < recommended_wattage * 0.8:
                power_status = {"status": "critical"}
            elif build["power_supply"].wattage < recommended_wattage:
                power_status = {"status": "warning"}
            else:
                power_status = {"status": "good"}
        else:
            power_status = {"status": "not_selected"}

    # Generate share URL
    share_url = request.build_absolute_uri()

    context = {
        "build": build,
        "components_price": components_price,
        "peripherals_price": peripherals_price,
        "assembly_fee": assembly_fee,
        "total_price": total_price,
        "discounts": Decimal("0"),  # Add discount logic if needed
        "is_buildable": is_buildable,
        "completion_percentage": completion_percentage,
        "essential_components_selected": essential_components_selected,  # Added this line to pass count to template
        "compatibility_status": compatibility_status,
        "power_status": power_status,
        "total_wattage": total_wattage,
        "recommended_wattage": recommended_wattage,
        "share_url": share_url,
    }

    return render(request, "pcbuilder/pc-builder.html", context)


def get_or_create_pc_builder(request):
    """
    Get existing PC builder instance or create a new one for the current user/session.

    This function handles PC builder instance management for both authenticated users
    and anonymous sessions. For authenticated users, it attempts to find an existing
    unnamed build or creates a new one. For anonymous users, it uses session-based
    tracking with a unique session ID.

    Args:
        request (HttpRequest): The HTTP request object containing user and session data.

    Returns:
        PCBuilder: The PC builder instance associated with the current user or session.
                  This will be either an existing build or a newly created one.

    Notes:
        - Authenticated users: Looks for builds with user=request.user and name=None
        - Anonymous users: Uses session_id stored in request.session
        - Creates new session_id (UUID4) if none exists for anonymous users
        - Only retrieves/creates unnamed builds (name=None) to distinguish from saved builds
    """
    if request.user.is_authenticated:
        # Try to get an existing PC build for the logged-in user
        pc_build = PCBuilder.objects.filter(user=request.user, name=None).first()
        if not pc_build:
            pc_build = PCBuilder.objects.create(user=request.user)
    else:
        # Use session for anonymous users
        session_id = request.session.get("pc_builder_session_id")
        if not session_id:
            session_id = str(uuid.uuid4())
            request.session["pc_builder_session_id"] = session_id

        pc_build = PCBuilder.objects.filter(session_id=session_id, name=None).first()
        if not pc_build:
            pc_build = PCBuilder.objects.create(session_id=session_id)

    return pc_build


def clear_build(request):
    """
    Clear all components from the current PC build.

    This view handles clearing all selected components from the user's current PC build.
    It supports both authenticated users (by clearing database records) and anonymous
    users (by clearing session data). Only processes POST requests for security.

    Args:
        request (HttpRequest): The HTTP request object. Must be a POST request to process.

    Returns:
        HttpResponseRedirect: Redirects to the PC builder page after clearing.

    Side Effects:
        - For authenticated users: Resets all PCBuilderItem fields to None
        - For anonymous users: Removes build-related session data
        - Displays success message to user
        - Only processes POST requests, ignores other HTTP methods

    Session Data Cleared (anonymous users):
        - build_id: The current build identifier
        - build_components: Component selection data
        - Any session keys starting with 'build_'
    """
    if request.method == "POST":
        if request.user.is_authenticated:
            # Get the current build for logged-in user
            build = get_or_create_pc_builder(request)
            if build:
                # Clear all components by resetting all PCBuilderItems
                for item in build.pcbuilderitem_set.all():
                    item.product_id = None
                    item.product_name = None
                    item.product_price = None
                    item.product_tdp = None
                    item.save()
        else:
            # Clear session data for anonymous users
            if "build_id" in request.session:
                del request.session["build_id"]
            if "build_components" in request.session:
                del request.session["build_components"]
            # Clear any other build-related session data
            for key in list(request.session.keys()):
                if key.startswith("build_"):
                    del request.session[key]
            request.session.modified = True

        messages.success(request, "Your PC build has been cleared successfully.")

    # Redirect back to PC builder page
    return redirect("pc_builder")


def initialize_pc_builder(pc_build):
    """
    Initialize PC builder with empty component slots for all component types.

    This function ensures that a PC builder instance has PCBuilderItem entries
    for all available component types. It creates empty slots that can later
    be populated with selected products.

    Args:
        pc_build (PCBuilder): The PC builder instance to initialize with component slots.

    Side Effects:
        Creates PCBuilderItem objects for each component type defined in
        PCBuilderItem.COMPONENT_CHOICES if they don't already exist.
        Each created item starts with no product selected (product_id=None).

    Notes:
        - Only creates items that don't already exist to avoid duplicates
        - Component types are derived from PCBuilderItem.COMPONENT_CHOICES
        - Each PCBuilderItem starts empty and ready for product assignment
    """
    for component_type, _ in PCBuilderItem.COMPONENT_CHOICES:
        # Check if item already exists
        if not PCBuilderItem.objects.filter(
            pc_builder=pc_build, component_type=component_type
        ).exists():
            PCBuilderItem.objects.create(
                pc_builder=pc_build, component_type=component_type
            )


def select_component(request, component_type):
    """
    Display component selection page with filtering, searching, and compatibility checking.

    This view renders a component selection interface for a specific component type
    within the PC Builder. It provides product filtering, compatibility checking
    with already selected components, search functionality, and sorting options.

    Args:
        request (HttpRequest): The HTTP request object containing query parameters.
        component_type (str): The type of component to display (e.g., 'CPU', 'GPU', 'RAM').
                             URL parameter that determines which product model to query.

    Returns:
        HttpResponse: Rendered component selection page with filtered products and options.

    Query Parameters:
        search (str): Search term for filtering products by brand, model, or description
        sort (str): Sorting option ('price_asc', 'price_desc', 'name_asc', 'newest')
        compatibility_filter (str): If 'on', filters out incompatible products
        filter_socket (str): Socket type filter for CPU/Motherboard components
        filter_form_factor (str): Form factor filter for Motherboard/Casing components
        filter_ram_type (str): RAM type filter for RAM components
        page (int): Page number for pagination (12 products per page)

    Context Variables:
        component_type (str): Display name for the component type
        products (Page): Paginated products with compatibility and stock information
        search_query (str): Current search term
        current_sort (str): Current sorting option
        compatibility_filtered (bool): Whether compatibility filter is active
        sockets (QuerySet): Available socket options for CPU/Motherboard
        form_factors (QuerySet): Available form factor options for Motherboard/Casing
        ram_types (QuerySet): Available RAM type options for RAM
        current_selection (Product|None): Currently selected product for this component type
        has_compatibility_check (bool): Whether compatibility checking is applicable

    Product Attributes Added:
        stock_status (str): 'In Stock', 'Low Stock', or 'Out of Stock'
        compatibility_issues (list): List of compatibility issue messages
        is_compatible (bool): Whether product is compatible with selected components

    Compatibility Checks:
        - CPU ↔ Motherboard: Socket matching
        - RAM ↔ Motherboard: Memory type matching
        - Power Supply: Wattage adequacy (total TDP + 100W buffer)
        - Casing ↔ Motherboard: Form factor compatibility

    Notes:
        - Handles component type mapping (e.g., 'CPU Cooler' → 'Cooler')
        - Filters products by is_available=True
        - Applies search across brand, model, and description fields
        - Supports component-specific filtering by technical specifications
    """
    pc_build = get_or_create_pc_builder(request)

    # Map the URL component type to the actual model type
    # This helps handle cases like "CPU Cooler" mapping to "Cooler" model
    component_type_mapping = {
        "CPU Cooler": "Cooler",
        # Add other mappings if needed in the future
    }

    # Get the mapped component type if it exists, otherwise use the original
    model_component_type = component_type_mapping.get(component_type, component_type)

    # Find which component models to use based on component_type
    component_models = {
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

    # Get all selected components to determine compatibility
    selected_components = {}
    for c_type in component_models.keys():
        try:
            item = PCBuilderItem.objects.get(pc_builder=pc_build, component_type=c_type)
            if item.product_id:
                selected_components[c_type] = item.get_product()
        except PCBuilderItem.DoesNotExist:
            pass

    # Get search query, sort choice, and compatibility filter preference
    search_query = request.GET.get("search", "")
    current_sort = request.GET.get("sort", "price_asc")
    compatibility_filtered = request.GET.get("compatibility_filter") == "on"

    # Component-specific filters
    selected_socket = request.GET.get("filter_socket", "")
    selected_form_factor = request.GET.get("filter_form_factor", "")
    selected_ram_type = request.GET.get("filter_ram_type", "")

    products = []
    current_selection = None

    # Initialize filter variables
    sockets = []
    form_factors = []
    ram_types = []

    if model_component_type not in component_models:
        # Handle 404 later
        pass
    else:
        model = component_models[model_component_type]

        # Start with all available products of this type
        queryset = model.objects.filter(is_available=True)

        # Apply search filter if provided
        if search_query:
            queryset = queryset.filter(
                models.Q(brand__icontains=search_query)
                | models.Q(model__icontains=search_query)
                | models.Q(description__icontains=search_query)
            )

        # Apply component-specific filters
        if model_component_type == "CPU" and selected_socket:
            queryset = queryset.filter(socket=selected_socket)

        if model_component_type == "Motherboard" and selected_socket:
            queryset = queryset.filter(socket=selected_socket)

        if model_component_type == "Motherboard" and selected_form_factor:
            queryset = queryset.filter(form_factor=selected_form_factor)

        if model_component_type == "Casing" and selected_form_factor:
            # For casing, form_factor is a field that should contain the selected form factor
            queryset = queryset.filter(form_factor__contains=selected_form_factor)

        if model_component_type == "RAM" and selected_ram_type:
            queryset = queryset.filter(ram_type=selected_ram_type)

        # Get the current selection for this component type
        try:
            # For CPU Cooler, we need to look up using the display component type
            # This maps back to how the component is stored in PCBuilderItem
            lookup_component_type = (
                component_type if component_type != "CPU Cooler" else "Cooler"
            )
            builder_item = PCBuilderItem.objects.get(
                pc_builder=pc_build, component_type=lookup_component_type
            )
            current_selection = (
                builder_item.get_product() if builder_item.product_id else None
            )
        except PCBuilderItem.DoesNotExist:
            current_selection = None

        # Process products and add compatibility information
        products = list(queryset)

        # Add stock status and compatibility status to all products
        for product in products:
            # Add stock status
            if product.stock > 10:
                product.stock_status = "In Stock"
            elif product.stock > 0:
                product.stock_status = "Low Stock"
            else:
                product.stock_status = "Out of Stock"

            # Check compatibility for each product
            product.compatibility_issues = []

            # CPU compatibility with Motherboard
            if model_component_type == "CPU" and "Motherboard" in selected_components:
                motherboard = selected_components["Motherboard"]
                if product.socket != motherboard.socket:
                    product.compatibility_issues.append(
                        f"Socket mismatch: CPU uses {product.socket} but motherboard has {motherboard.socket}"
                    )

            # Motherboard compatibility with CPU
            elif model_component_type == "Motherboard" and "CPU" in selected_components:
                cpu = selected_components["CPU"]
                if cpu.socket != product.socket:
                    product.compatibility_issues.append(
                        f"Socket mismatch: Motherboard has {product.socket} but CPU uses {cpu.socket}"
                    )

            # RAM compatibility with Motherboard
            elif model_component_type == "RAM" and "Motherboard" in selected_components:
                motherboard = selected_components["Motherboard"]
                if product.ram_type != motherboard.memory_type:
                    product.compatibility_issues.append(
                        f"Memory type mismatch: RAM is {product.ram_type} but motherboard supports {motherboard.memory_type}"
                    )

            # Motherboard compatibility with RAM
            elif model_component_type == "Motherboard" and "RAM" in selected_components:
                ram = selected_components["RAM"]
                if ram.ram_type != product.memory_type:
                    product.compatibility_issues.append(
                        f"Memory type mismatch: Motherboard supports {product.memory_type} but RAM is {ram.ram_type}"
                    )

            # Power Supply compatibility check
            elif model_component_type == "Power Supply":
                total_tdp = sum(
                    getattr(comp, "tdp", 0) or 0
                    for comp in selected_components.values()
                )
                # Add 100W buffer
                recommended_wattage = total_tdp + 100
                if product.wattage < recommended_wattage:
                    product.compatibility_issues.append(
                        f"Insufficient wattage: Your components need at least {recommended_wattage}W, but this PSU provides {product.wattage}W"
                    )

            # Case compatibility with Motherboard
            elif (
                model_component_type == "Casing"
                and "Motherboard" in selected_components
            ):
                motherboard = selected_components["Motherboard"]
                if motherboard.form_factor not in product.form_factor:
                    product.compatibility_issues.append(
                        f"Form factor mismatch: Case supports {product.form_factor} but motherboard is {motherboard.form_factor}"
                    )

            # Motherboard compatibility with Case
            elif (
                model_component_type == "Motherboard"
                and "Casing" in selected_components
            ):
                case = selected_components["Casing"]
                if product.form_factor not in case.form_factor:
                    product.compatibility_issues.append(
                        f"Form factor mismatch: Motherboard is {product.form_factor} but case supports {case.form_factor}"
                    )

            # Set compatibility status
            product.is_compatible = len(product.compatibility_issues) == 0

        # If compatibility filter is enabled, filter out incompatible products
        if compatibility_filtered:
            products = [p for p in products if p.is_compatible]

        # Apply sorting
        if current_sort == "price_asc":
            products = sorted(products, key=lambda x: x.price or 0)
        elif current_sort == "price_desc":
            products = sorted(products, key=lambda x: x.price or 0, reverse=True)
        elif current_sort == "name_asc":
            products = sorted(products, key=lambda x: f"{x.brand} {x.model}")
        elif current_sort == "newest":
            products = sorted(
                products,
                key=lambda x: x.created_at
                if hasattr(x, "created_at")
                else datetime.now(),
                reverse=True,
            )

        # Get filters for the dropdown menus
        if model_component_type == "CPU" or model_component_type == "Motherboard":
            # Get distinct socket values from the model
            sockets = model.objects.values_list("socket", flat=True).distinct()

        if model_component_type == "Motherboard" or model_component_type == "Casing":
            # Get distinct form factor values
            form_factors = model.objects.values_list(
                "form_factor", flat=True
            ).distinct()

        if model_component_type == "RAM":
            # Get distinct RAM types
            ram_types = model.objects.values_list("ram_type", flat=True).distinct()

        # For Cooler, get available socket support values
        if model_component_type == "Cooler":
            # This may need special handling since socket_support is often a comma-separated string
            pass

    # Check for pagination
    paginator = Paginator(products, 12)  # Show 12 components per page
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    # Map some component types to a more user-friendly display name
    display_component_type = component_type

    context = {
        "component_type": display_component_type,
        "products": page_obj,
        "search_query": search_query,
        "current_sort": current_sort,
        "compatibility_filtered": compatibility_filtered,
        "sockets": sockets,
        "selected_socket": selected_socket,
        "form_factors": form_factors,
        "selected_form_factor": selected_form_factor,
        "ram_types": ram_types,
        "selected_ram_type": selected_ram_type,
        "current_selection": current_selection,
        "has_compatibility_check": bool(
            selected_components
        ),  # Indicates if compatibility checking is relevant
    }

    return render(request, "pcbuilder/pc-builder-select.html", context)


@csrf_exempt
def add_component_to_build(request):
    """
    Add a selected component to the user's PC build configuration.

    This AJAX endpoint handles adding products to the PC build by creating or updating
    PCBuilderItem entries. It supports both JSON and form data submission and includes
    special handling for storage components and power supply compatibility checking.

    Args:
        request (HttpRequest): The HTTP request object. Must be a POST request.
                              Supports both JSON and form data content types.

    Returns:
        JsonResponse: JSON response with operation status and updated build information.

    Request Data (JSON or Form):
        product_id (str): The ID of the product to add to the build
        component_type (str): The type of component being added (e.g., 'CPU', 'GPU')

    Response Format:
        Success Response:
            status (str): 'success'
            message (str): Confirmation message with product details
            total_price (float): Updated total build price
            recommended_wattage (int): Updated recommended PSU wattage

        Error Response:
            status (str): 'error'
            message (str): Error description

    Special Handling:
        - Storage Components: Automatically determines SSD vs HDD based on product ID
        - Power Supply Aliases: Handles both 'Power Supply' and 'PowerSupply'
        - Compatibility Checking: Runs compatibility check but doesn't block selection
        - Product Validation: Verifies product exists and is available

    Side Effects:
        - Creates or updates PCBuilderItem with product details
        - Stores product_id, product_name, product_price, and product_tdp
        - Updates build totals and power calculations
        - Logs component addition for debugging

    Error Conditions:
        - Missing product_id or component_type
        - Invalid component type
        - Product not found in specified component model
        - Invalid JSON data format
        - Non-POST request method

    Notes:
        - CSRF exempt for AJAX compatibility
        - Supports both authenticated and anonymous users
        - Handles component type mapping for database storage
    """
    if request.method == "POST":
        try:
            # Check if it's a JSON request or form data
            if request.content_type and "application/json" in request.content_type:
                # Handle JSON data
                data = json.loads(request.body)
                product_id = data.get("product_id")
                component_type = data.get("component_type")
            else:
                # Handle form data
                product_id = request.POST.get("product_id")
                component_type = request.POST.get("component_type")

            if not product_id or not component_type:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "Missing product ID or component type",
                    }
                )

            # Debug log to trace the issue
            print(f"Adding component: {component_type}, Product ID: {product_id}")

            # Map component_type to model
            component_models = {
                "CPU": CPU,
                "Cooler": Cooler,
                "Motherboard": Motherboard,
                "RAM": RAM,
                "SSD": SSD,
                "HDD": HDD,
                "GPU": GPU,
                "Power Supply": PowerSupply,
                "PowerSupply": PowerSupply,  # Alias for Power Supply
                "Casing": Casing,
                "Monitor": Monitor,
                "Keyboard": Keyboard,
                "Mouse": Mouse,
                "Headphone": Headphone,
            }

            # Handle 'Storage' component type which could be either SSD or HDD
            if component_type == "Storage":
                # Try to determine if this is an SSD or HDD based on form submission or URL
                # Check if the ID exists in SSD model, if not, try HDD
                try:
                    SSD.objects.get(id=product_id)
                    component_type = "SSD"
                except SSD.DoesNotExist:
                    try:
                        HDD.objects.get(id=product_id)
                        component_type = "HDD"
                    except HDD.DoesNotExist:
                        return JsonResponse(
                            {
                                "status": "error",
                                "message": f"Storage product with ID {product_id} not found",
                            }
                        )

            if component_type not in component_models:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": f"Invalid component type: {component_type}",
                    }
                )

            # Get the product
            model = component_models[component_type]
            try:
                product = model.objects.get(id=product_id)
            except model.DoesNotExist:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": f"Product not found for {component_type} with ID {product_id}",
                    }
                )

            # Get the PC build
            pc_build = get_or_create_pc_builder(request)

            # Check compatibility (but don't block selection)
            check_compatibility(pc_build, component_type, product)

            # Update the PC builder item
            builder_item, created = PCBuilderItem.objects.get_or_create(
                pc_builder=pc_build, component_type=component_type
            )

            builder_item.product_id = product.id
            builder_item.product_name = f"{product.brand} {product.model}"
            builder_item.product_price = product.price
            builder_item.product_tdp = product.tdp
            builder_item.save()

            # Return updated build information
            return JsonResponse(
                {
                    "status": "success",
                    "message": f"{product.brand} {product.model} added to your build",
                    "total_price": float(pc_build.get_total_price),
                    "recommended_wattage": pc_build.get_recommended_wattage,
                }
            )

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request method"})


def remove_component_from_build(request, component_type):
    """
    Remove a specific component from the user's PC build configuration.

    This endpoint handles removing components from the PC build by clearing the
    product reference in the corresponding PCBuilderItem. It supports both AJAX
    and traditional form submissions and includes special handling for storage
    components and CPU coolers.

    Args:
        request (HttpRequest): The HTTP request object. Must be a POST request.
        component_type (str): The type of component to remove from the build.
                             URL parameter specifying which component to clear.

    Returns:
        JsonResponse|HttpResponseRedirect: JSON response for AJAX requests,
                                          redirect to PC builder for traditional requests.

    Response Format (AJAX):
        Success Response:
            status (str): 'success'
            message (str): Confirmation message
            total_price (float): Updated total build price
            recommended_wattage (int): Updated recommended PSU wattage

        Error Response:
            status (str): 'error'
            message (str): Error description

    Special Handling:
        - CPU Cooler: Maps 'CPU Cooler' URL parameter to 'Cooler' database type
        - Storage: Removes both SSD and HDD components when 'Storage' is specified
        - Component Validation: Checks if component exists before removal
        - Request Detection: Automatically detects AJAX vs traditional requests

    Side Effects:
        - Clears product_id, product_name, product_price, and product_tdp fields
        - Preserves PCBuilderItem record structure for future selections
        - Updates build totals and power calculations
        - Displays success/error messages for non-AJAX requests

    Error Conditions:
        - Component not found in build
        - No storage components found (for Storage type)
        - PCBuilderItem does not exist for specified component type
        - Non-POST request: Redirects without deletion

    Notes:
        - Supports both authenticated and anonymous users
        - Maintains build structure by keeping empty PCBuilderItem records
        - Handles dual storage removal for comprehensive storage clearing
        - Provides appropriate user feedback through messages or JSON responses
    """
    if request.method == "POST":
        try:
            # Get the PC build
            pc_build = get_or_create_pc_builder(request)

            # Handle special case for CPU Cooler (maps to Cooler in the database)
            if component_type == "CPU Cooler":
                component_type = "Cooler"

            # Handle special case for Storage (could be SSD or HDD)
            if component_type == "Storage":
                # Check if SSD is present and remove it
                ssd_removed = False
                try:
                    ssd_item = PCBuilderItem.objects.get(
                        pc_builder=pc_build, component_type="SSD"
                    )
                    if ssd_item.product_id:
                        ssd_item.product_id = None
                        ssd_item.product_name = None
                        ssd_item.product_price = None
                        ssd_item.product_tdp = None
                        ssd_item.save()
                        ssd_removed = True
                except PCBuilderItem.DoesNotExist:
                    pass

                # Check if HDD is present and remove it
                hdd_removed = False
                try:
                    hdd_item = PCBuilderItem.objects.get(
                        pc_builder=pc_build, component_type="HDD"
                    )
                    if hdd_item.product_id:
                        hdd_item.product_id = None
                        hdd_item.product_name = None
                        hdd_item.product_price = None
                        hdd_item.product_tdp = None
                        hdd_item.save()
                        hdd_removed = True
                except PCBuilderItem.DoesNotExist:
                    pass

                # If neither was removed, it's an error
                if not ssd_removed and not hdd_removed:
                    if request.headers.get(
                        "X-Requested-With"
                    ) == "XMLHttpRequest" or "application/json" in request.headers.get(
                        "Content-Type", ""
                    ):
                        return JsonResponse(
                            {
                                "status": "error",
                                "message": "No storage components found in build",
                            }
                        )
                    else:
                        messages.error(request, "No storage components found in build.")
                        return redirect("pc_builder")

                # Handle successful removal
                if request.headers.get(
                    "X-Requested-With"
                ) == "XMLHttpRequest" or "application/json" in request.headers.get(
                    "Content-Type", ""
                ):
                    return JsonResponse(
                        {
                            "status": "success",
                            "message": "Storage removed from your build",
                            "total_price": float(pc_build.get_total_price),
                            "recommended_wattage": pc_build.get_recommended_wattage,
                        }
                    )
                else:
                    messages.success(request, "Storage removed from your build.")
                    return redirect("pc_builder")

            # For all other component types, proceed as normal
            try:
                builder_item = PCBuilderItem.objects.get(
                    pc_builder=pc_build, component_type=component_type
                )

                # Clear the product reference but keep the item
                builder_item.product_id = None
                builder_item.product_name = None
                builder_item.product_price = None
                builder_item.product_tdp = None
                builder_item.save()

                # Check if it's an AJAX request
                if request.headers.get(
                    "X-Requested-With"
                ) == "XMLHttpRequest" or "application/json" in request.headers.get(
                    "Content-Type", ""
                ):
                    # Return JSON response for AJAX calls
                    return JsonResponse(
                        {
                            "status": "success",
                            "message": f"{component_type} removed from your build",
                            "total_price": float(pc_build.get_total_price),
                            "recommended_wattage": pc_build.get_recommended_wattage,
                        }
                    )
                else:
                    # For non-AJAX requests, redirect to PC builder page
                    messages.success(
                        request, f"{component_type} removed from your build."
                    )
                    return redirect("pc_builder")

            except PCBuilderItem.DoesNotExist:
                if request.headers.get(
                    "X-Requested-With"
                ) == "XMLHttpRequest" or "application/json" in request.headers.get(
                    "Content-Type", ""
                ):
                    return JsonResponse(
                        {"status": "error", "message": "Component not found in build"}
                    )
                else:
                    messages.error(request, "Component not found in build.")
                    return redirect("pc_builder")

        except Exception as e:
            if request.headers.get(
                "X-Requested-With"
            ) == "XMLHttpRequest" or "application/json" in request.headers.get(
                "Content-Type", ""
            ):
                return JsonResponse({"status": "error", "message": str(e)})
            else:
                messages.error(request, f"Error removing component: {str(e)}")
                return redirect("pc_builder")

    # Default fallback for non-POST requests
    return redirect("pc_builder")


def check_compatibility(pc_build, new_component_type, new_product):
    """
    Check hardware compatibility between a new component and existing build components.

    This function analyzes compatibility between a newly selected component and all
    currently selected components in the PC build. It checks for common compatibility
    issues like socket mismatches, memory type conflicts, power requirements, and
    form factor incompatibilities.

    Args:
        pc_build (PCBuilder): The PC builder instance containing current components.
        new_component_type (str): The type of the new component being added
                                 (e.g., 'CPU', 'Motherboard', 'RAM').
        new_product (Model): The product model instance being added to the build.
                            Should have relevant technical specifications.

    Returns:
        list: A list of compatibility issue messages (strings). Empty list if
              no compatibility issues are found.

    Compatibility Checks Performed:
        CPU ↔ Motherboard:
            - Socket type matching (e.g., LGA1700, AM4)

        RAM ↔ Motherboard:
            - Memory type compatibility (e.g., DDR4, DDR5)

        Power Supply:
            - Wattage adequacy check (total component TDP + 100W buffer)

        Casing ↔ Motherboard:
            - Form factor compatibility (e.g., ATX, Micro-ATX, Mini-IT)

    Technical Specifications Used:
        - CPU: socket, tdp
        - Motherboard: socket, memory_type, form_factor, tdp
        - RAM: ram_type, tdp
        - Power Supply: wattage
        - Casing: form_factor (should contain supported form factors)
        - Other components: tdp (for power calculation)

    Notes:
        - Does not block component selection, only reports issues
        - Power calculation includes 100W safety buffer
        - Form factor checking handles both single and multiple supported formats
        - Excludes the new component from existing component analysis
        - Returns descriptive error messages for user understanding
    """
    compatibility_issues = []

    # Get all currently selected components
    selected_components = {}
    for item in pc_build.pcbuilderitem_set.all():
        if item.product_id and item.component_type != new_component_type:
            selected_components[item.component_type] = item.get_product()

    # CPU and Motherboard compatibility check
    if new_component_type == "CPU" and "Motherboard" in selected_components:
        motherboard = selected_components["Motherboard"]
        if new_product.socket != motherboard.socket:
            compatibility_issues.append(
                f"Socket mismatch: CPU uses {new_product.socket} but motherboard has {motherboard.socket}"
            )

    elif new_component_type == "Motherboard" and "CPU" in selected_components:
        cpu = selected_components["CPU"]
        if cpu.socket != new_product.socket:
            compatibility_issues.append(
                f"Socket mismatch: Motherboard has {new_product.socket} but CPU uses {new_product.socket}"
            )

    # RAM and Motherboard compatibility check
    if new_component_type == "RAM" and "Motherboard" in selected_components:
        motherboard = selected_components["Motherboard"]
        if new_product.ram_type != motherboard.memory_type:
            compatibility_issues.append(
                f"Memory type mismatch: RAM is {new_product.ram_type} but motherboard supports {motherboard.memory_type}"
            )

    elif new_component_type == "Motherboard" and "RAM" in selected_components:
        ram = selected_components["RAM"]
        if ram.ram_type != new_product.memory_type:
            compatibility_issues.append(
                f"Memory type mismatch: Motherboard supports {new_product.memory_type} but RAM is {ram.ram_type}"
            )

    # Power supply wattage check for all components
    if new_component_type == "Power Supply":
        total_tdp = sum(
            getattr(comp, "tdp", 0) or 0 for comp in selected_components.values()
        )
        # Add 100W buffer
        recommended_wattage = total_tdp + 100
        if new_product.wattage < recommended_wattage:
            compatibility_issues.append(
                f"Insufficient wattage: Your components need at least {recommended_wattage}W, but this PSU provides {new_product.wattage}W"
            )

    # Case and Motherboard compatibility check
    if new_component_type == "Casing" and "Motherboard" in selected_components:
        motherboard = selected_components["Motherboard"]
        if motherboard.form_factor not in new_product.form_factor:
            compatibility_issues.append(
                f"Form factor mismatch: Case supports {new_product.form_factor} but motherboard is {motherboard.form_factor}"
            )

    elif new_component_type == "Motherboard" and "Casing" in selected_components:
        case = selected_components["Casing"]
        if new_product.form_factor not in case.form_factor:
            compatibility_issues.append(
                f"Form factor mismatch: Motherboard is {new_product.form_factor} but case supports {case.form_factor}"
            )

    return compatibility_issues


@login_required
def save_pc_build(request):
    """
    Save the current PC build configuration with a user-defined name.

    This view allows authenticated users to save their current PC build configuration
    as a named build for future reference or sharing. It creates a copy of the current
    build with all selected components preserved.

    Args:
        request (HttpRequest): The HTTP request object. Must be a POST request.
                              User must be authenticated (enforced by @login_required).

    Returns:
        HttpResponseRedirect: Redirects to the PC builder page after save operation.

    Request Data (POST):
        build_name (str): The name to assign to the saved build (required)
        is_public (str): Whether the build should be public ('on' for public)

    Side Effects:
        - Creates a new PCBuilder instance with the provided name
        - Copies all PCBuilderItem entries from current build to saved build
        - Only saves components that have products selected (product_id is not None)
        - Preserves all component details (type, product_id, name, price, tdp)
        - Displays success message upon completion

    Error Conditions:
        - Missing build_name: Displays error message and redirects
        - Non-POST requests: Redirects to PC builder page
        - User not authenticated: Redirects to login (handled by decorator)

    Notes:
        - Creates a complete copy, not a reference to the original build
        - Original current build remains unchanged and usable
        - Saved builds are distinguished by having a non-null name field
        - Public builds can be viewed by other users (feature dependent)
        - Build creation timestamp is automatically set
    """
    if request.method == "POST":
        build_name = request.POST.get("build_name")
        is_public = request.POST.get("is_public") == "on"

        if not build_name:
            messages.error(request, "Please provide a name for your build")
            return redirect("pc_builder")

        # Get the current build
        current_build = get_or_create_pc_builder(request)

        # Create a new saved build with the provided name
        saved_build = PCBuilder.objects.create(
            user=request.user, name=build_name, is_public=is_public
        )

        # Copy all components from current build to saved build
        for item in current_build.pcbuilderitem_set.all():
            if item.product_id:
                PCBuilderItem.objects.create(
                    pc_builder=saved_build,
                    component_type=item.component_type,
                    product_id=item.product_id,
                    product_name=item.product_name,
                    product_price=item.product_price,
                    product_tdp=item.product_tdp,
                )

        messages.success(request, f"Build '{build_name}' saved successfully!")
        return redirect("pc_builder")

    return redirect("pc_builder")


@login_required
def my_saved_builds(request):
    """
    Display a list of all saved PC builds for the authenticated user.

    This view renders a page showing all PC builds that the current user has
    saved with names. Builds are ordered by creation date (newest first) for
    easy browsing and management.

    Args:
        request (HttpRequest): The HTTP request object. User must be authenticated.

    Returns:
        HttpResponse: Rendered page displaying the user's saved builds.

    Context Variables:
        builds (QuerySet): Ordered list of user's saved PCBuilder instances.
                          Filtered to only include named builds (name__isnull=False).
                          Ordered by creation date (newest first).

    Query Details:
        - Filters by user=request.user to show only current user's builds
        - Excludes current working builds by requiring name__isnull=False
        - Orders by -created_at for reverse chronological display

    Notes:
        - Only shows saved builds, not the current working build
        - User authentication required (enforced by @login_required decorator)
        - Each build in the list includes all associated components and metadata
        - Template can access build details like name, creation date, total price
    """
    builds = PCBuilder.objects.filter(user=request.user, name__isnull=False).order_by(
        "-created_at"
    )

    context = {"builds": builds}

    return render(request, "pcbuilder/my-saved-builds.html", context)


@login_required
def load_saved_build(request, build_id):
    """
    Load a saved PC build configuration into the current PC Builder workspace.

    This view allows users to load a previously saved build into their current
    PC Builder workspace for editing or purchasing. It replaces all components
    in the current build with those from the selected saved build.

    Args:
        request (HttpRequest): The HTTP request object. User must be authenticated.
        build_id (int): The ID of the saved build to load. URL parameter.

    Returns:
        HttpResponseRedirect: Redirects to the PC builder page with loaded build.

    Side Effects:
        - Clears all components from the current working build
        - Copies all components from the saved build to the current build
        - Creates PCBuilderItem entries for each component in the saved build
        - Preserves all component details (type, product_id, name, price, tdp)
        - Displays success message with the loaded build name

    Error Conditions:
        - Build not found: Returns 404 error
        - Build belongs to different user: Returns 404 error (security)
        - User not authenticated: Redirects to login (handled by decorator)
        - Non-POST request: Redirects without deletion

    Security:
        - Only allows users to load their own builds (user=request.user filter)
        - Uses get_object_or_404 for safe build retrieval

    Notes:
        - Completely replaces current build contents
        - Does not modify the original saved build
        - Only copies components that have products selected (product_id is not None)
        - Current build retains its identity but gets new component configuration
        - Initializes current build structure if it doesn't exist
    """
    # Get the saved build
    saved_build = get_object_or_404(PCBuilder, id=build_id, user=request.user)

    # Get or create the current build
    current_build = get_or_create_pc_builder(request)

    # Clear the current build
    current_build.pcbuilderitem_set.all().update(
        product_id=None, product_name=None, product_price=None, product_tdp=None
    )

    # Copy components from saved build to current build
    for item in saved_build.pcbuilderitem_set.all():
        if item.product_id:
            current_item, created = PCBuilderItem.objects.get_or_create(
                pc_builder=current_build, component_type=item.component_type
            )

            current_item.product_id = item.product_id
            current_item.product_name = item.product_name
            current_item.product_price = item.product_price
            current_item.product_tdp = item.product_tdp
            current_item.save()

    messages.success(request, f"Build '{saved_build.name}' loaded successfully!")
    return redirect("pc_builder")


@login_required
def delete_saved_build(request, build_id):
    """
    Delete a saved PC build from the user's collection.

    This view handles the permanent deletion of a saved PC build. It provides
    a secure way for users to remove builds they no longer need while ensuring
    only the build owner can perform the deletion.

    Args:
        request (HttpRequest): The HTTP request object. Must be a POST request.
                              User must be authenticated.
        build_id (int): The ID of the saved build to delete. URL parameter.

    Returns:
        HttpResponseRedirect: Redirects to the saved builds list page.

    Side Effects:
        - Permanently deletes the PCBuilder instance and all associated PCBuilderItems
        - Displays success message with the deleted build name
        - Only processes POST requests for security (ignores GET)

    Error Conditions:
        - Build not found: Returns 404 error
        - Build belongs to different user: Returns 404 error (security)
        - User not authenticated: Redirects to login (handled by decorator)
        - Non-POST request: Redirects without deletion

    Security:
        - POST-only operation to prevent accidental deletion via GET requests
        - Only allows users to delete their own builds (user=request.user filter)
        - Uses get_object_or_404 for safe build retrieval

    Notes:
        - Deletion is permanent and cannot be undone
        - Cascading deletion removes all associated PCBuilderItem records
        - Preserves build name for confirmation message before deletion
        - Does not affect the user's current working build
    """
    if request.method == "POST":
        build = get_object_or_404(PCBuilder, id=build_id, user=request.user)
        build_name = build.name or "Unnamed Build"
        build.delete()
        messages.success(request, f"Build '{build_name}' deleted successfully.")

    return redirect("my_saved_builds")


@login_required
def add_build_to_cart(request, build_id=None):
    """
    Add all components from a PC build to the user's shopping cart.

    This view transfers all components from either a saved build or the current
    working build into the user's shopping cart for purchase. It performs stock
    validation and handles duplicate items appropriately.

    Args:
        request (HttpRequest): The HTTP request object. User must be authenticated.
        build_id (int, optional): ID of a saved build to add to cart. If None,
                                 uses the current working build.

    Returns:
        HttpResponseRedirect: Redirects to cart view on success, PC builder on error.

    Side Effects:
        - Creates CartItem entries for each component in the build
        - Increments quantity if component already exists in cart
        - Validates stock availability before adding items
        - Displays success/error messages based on operation results

    Stock Validation:
        - Checks stock levels for all components before adding any to cart
        - Prevents adding out-of-stock items (stock <= 0)
        - Reports all out-of-stock items in error message
        - Fails entire operation if any component is unavailable

    Cart Behavior:
        - Creates new CartItem if component not in cart
        - Increments quantity by 1 if component already in cart
        - Sets product_category to component_type for proper categorization
        - Uses current product price from PCBuilderItem

    Error Conditions:
        - Build not found: Returns 404 error
        - Build belongs to different user: Returns 404 error (for saved builds)
        - Out of stock components: Shows error and redirects to PC builder
        - Empty build: Shows warning message
        - User not authenticated: Redirects to login (handled by decorator)

    Success Response:
        - Shows count of components added to cart
        - Redirects to cart view for immediate review/checkout

    Notes:
        - Only adds components that have products selected (product_id is not None)
        - Uses CartApp.views.get_cart to retrieve user's cart instance
        - Maintains cart integrity by checking existing items before creation
        - Provides clear feedback on operation success or failure
    """
    # Determine which build to use
    if build_id:
        # Use a saved build
        pc_build = get_object_or_404(PCBuilder, id=build_id, user=request.user)
    else:
        # Use the current build
        pc_build = get_or_create_pc_builder(request)

    # Get the user's cart
    from CartApp.views import get_cart

    cart = get_cart(request)

    # Check if any component is out of stock
    out_of_stock = []
    for item in pc_build.pcbuilderitem_set.all():
        if item.product_id:
            product = item.get_product()
            if product and product.stock <= 0:
                out_of_stock.append(f"{item.product_name}")

    if out_of_stock:
        messages.error(
            request,
            f"Cannot add to cart. The following items are out of stock: {', '.join(out_of_stock)}",
        )
        return redirect("pc_builder")

    # Add each component to the cart
    added_count = 0
    for item in pc_build.pcbuilderitem_set.all():
        if item.product_id:
            product = item.get_product()
            if product:
                # Check if already in cart
                from CartApp.models import CartItem

                try:
                    cart_item = CartItem.objects.get(
                        cart=cart,
                        product_id=item.product_id,
                        product_category=item.component_type,
                    )
                    # Update quantity if already in cart
                    cart_item.quantity += 1
                    cart_item.save()
                except CartItem.DoesNotExist:
                    # Create new cart item
                    CartItem.objects.create(
                        cart=cart,
                        product_id=item.product_id,
                        product_category=item.component_type,
                        quantity=1,
                        price=item.product_price,
                    )
                added_count += 1

    if added_count > 0:
        messages.success(request, f"{added_count} components added to your cart!")
    else:
        messages.warning(
            request,
            "No components were added to your cart. Please add components to your build first.",
        )

    return redirect("view_cart")


def export_build_pdf(request, build_id=None):
    """
    Export a PC build configuration as a professionally formatted PDF document.

    This view generates a comprehensive PDF report of a PC build with TechReform BD
    branding, complete component listing, compatibility analysis, pricing breakdown,
    and professional styling. The PDF includes company branding, detailed component
    specifications, and build analysis suitable for customer reference or quotation.

    Args:
        request (HttpRequest): The HTTP request object.
        build_id (int, optional): ID of a saved build to export. If None and user
                                 is authenticated, uses current working build.
                                 For anonymous users, always uses current build.

    Returns:
        HttpResponse: PDF file download response with appropriate headers, or
                     redirect to PC builder on error.

    PDF Content Structure:
        - Header with TechReform BD branding and build information
        - Build name and generation timestamp
        - Component list table with type, product details, and pricing
        - Compatibility status and any issues found
        - Power analysis with wattage requirements and PSU adequacy
        - Price breakdown (components, peripherals, assembly fee, total)
        - Professional footer with company information and disclaimers
        - Page numbering for multi-page builds

    PDF Styling Features:
        - TechReform BD brand colors and typography
        - Professional table formatting with proper column widths
        - Text wrapping for long component names
        - Color-coded compatibility indicators
        - Responsive layout for various component list lengths
        - High-quality formatting suitable for business use

    Technical Requirements:
        - Uses ReportLab library for PDF generation
        - A4 page size with professional margins
        - Brand color scheme matching TechReform website
        - Proper text wrapping and table formatting
        - Error handling for missing components or generation failures

    Error Conditions:
        - Build not found: Returns 404 error
        - Build access denied: Returns 404 for security
        - PDF generation failure: Shows error message and redirects
        - Missing ReportLab dependencies: Shows import error

    Security:
        - Only allows access to user's own saved builds
        - Anonymous users can only export current working build
        - No sensitive information exposed in PDF

    File Naming:
        - Uses build name if available, sanitized for filesystem
        - Falls back to "TechReform_PC_Build" for unnamed builds
        - Includes .pdf extension automatically

    Notes:
        - PDF generation is memory-intensive for large builds
        - Includes live pricing at time of generation
        - Contains disclaimer about price validity
        - Supports both single and multi-page layouts
        - Optimized for printing and digital sharing
    """
    try:
        # Import required modules
        from reportlab.lib.enums import TA_CENTER, TA_RIGHT
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import (
            SimpleDocTemplate,
            Paragraph,
            Spacer,
            Image,
            Table,
            TableStyle,
            HRFlowable,
        )
        from reportlab.lib import colors
        from reportlab.lib.units import mm
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet

        # Determine which build to use
        if build_id and request.user.is_authenticated:
            # Use a saved build
            pc_build = get_object_or_404(PCBuilder, id=build_id, user=request.user)
        else:
            # Use the current build
            pc_build = get_or_create_pc_builder(request)

        # Create a PDF
        buffer = BytesIO()

        # Use A4 for a standard international page size
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=15 * mm,
            leftMargin=15 * mm,
            topMargin=20 * mm,
            bottomMargin=20 * mm,
            title=f"TechReform PC Build - {pc_build.name if pc_build.name else 'Custom Build'}",
        )

        # Container for the 'Flowable' objects
        elements = []

        # Define styles
        styles = getSampleStyleSheet()

        # Define TechReform brand colors
        # Main colors from the website
        tech_blue = colors.HexColor("#0052D4")  # Primary brand color
        tech_light_blue = colors.HexColor("#65A7FB")  # Secondary brand color
        tech_dark = colors.HexColor("#333333")  # Text color
        tech_light_gray = colors.HexColor("#F5F5F5")  # Background color
        tech_accent = colors.HexColor("#FF6B21")  # Accent/highlight color
        tech_success = colors.HexColor("#4CAF50")  # Success/compatible color
        tech_error = colors.HexColor("#D32F2F")  # Error/warning color

        # Custom styles with TechReform website colors and proper text wrapping
        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Title"],
            fontSize=24,
            alignment=TA_CENTER,
            spaceAfter=6 * mm,
            textColor=tech_blue,
            fontName="Helvetica-Bold",
            wordWrap="CJK",  # Enable proper text wrapping
        )

        subtitle_style = ParagraphStyle(
            "CustomSubtitle",
            parent=styles["Heading2"],
            fontSize=16,
            spaceBefore=6 * mm,
            spaceAfter=3 * mm,
            textColor=tech_blue,
            borderPadding=5,
            borderWidth=0,
            borderRadius=3,
            borderColor=tech_light_blue,
            backColor=tech_light_gray,
            wordWrap="CJK",  # Enable proper text wrapping
        )

        normal_style = ParagraphStyle(
            "CustomNormal",
            parent=styles["Normal"],
            fontSize=10,
            leading=14,
            spaceAfter=3 * mm,
            textColor=tech_dark,
            wordWrap="CJK",  # Enable proper text wrapping
            allowWidows=0,  # Prevent single words on their own line
            allowOrphans=0,  # Prevent single words at start of paragraph
        )

        info_style = ParagraphStyle(
            "CustomInfo",
            parent=styles["Normal"],
            fontSize=10,
            backColor=colors.HexColor("#E5F3FF"),
            borderColor=tech_light_blue,
            borderWidth=1,
            borderPadding=8,
            borderRadius=5,
            spaceAfter=4 * mm,
            textColor=tech_dark,
            wordWrap="CJK",  # Enable proper text wrapping
        )

        warning_style = ParagraphStyle(
            "CustomWarning",
            parent=styles["Normal"],
            fontSize=10,
            textColor=tech_error,
            leftIndent=5 * mm,
            wordWrap="CJK",  # Enable proper text wrapping
        )

        compatible_style = ParagraphStyle(
            "CustomCompatible",
            parent=styles["Normal"],
            fontSize=10,
            textColor=tech_success,
            wordWrap="CJK",  # Enable proper text wrapping
        )

        footer_style = ParagraphStyle(
            "CustomFooter",
            parent=styles["Normal"],
            fontSize=8,
            textColor=colors.gray,
            alignment=TA_CENTER,
            fontName="Helvetica-Oblique",
            wordWrap="CJK",  # Enable proper text wrapping
        )

        price_style = ParagraphStyle(
            "PriceStyle",
            parent=styles["Normal"],
            fontSize=14,
            textColor=tech_accent,
            alignment=TA_RIGHT,
            fontName="Helvetica-Bold",
            wordWrap="CJK",  # Enable proper text wrapping
        )

        component_style = ParagraphStyle(
            "ComponentStyle",
            parent=styles["Normal"],
            fontSize=10,
            textColor=tech_dark,
            wordWrap="CJK",  # Enable proper text wrapping
            leading=12,  # Slightly tighter line spacing
            allowWidows=0,  # Prevent single words on their own line
            allowOrphans=0,  # Prevent single words at start of paragraph
        )

        # Add logo - Safely handle the case where STATIC_ROOT might be None
        try:
            # First try to find the logo in the static folder
            base_dir = settings.BASE_DIR  # This should always be defined
            possible_logo_paths = [
                os.path.join(base_dir, "static", "base", "images", "logo.png"),
                os.path.join(base_dir, "static", "index", "images", "logo.png"),
                os.path.join(base_dir, "static", "index", "img", "logo.png"),
                os.path.join(base_dir, "static", "theme", "img", "logo.png"),
            ]

            # Check if STATIC_ROOT is defined and add it as a possible location
            if hasattr(settings, "STATIC_ROOT") and settings.STATIC_ROOT:
                possible_logo_paths.append(
                    os.path.join(settings.STATIC_ROOT, "base", "images", "logo.png")
                )
                possible_logo_paths.append(
                    os.path.join(settings.STATIC_ROOT, "index", "images", "logo.png")
                )
                possible_logo_paths.append(
                    os.path.join(settings.STATIC_ROOT, "index", "img", "logo.png")
                )
                possible_logo_paths.append(
                    os.path.join(settings.STATIC_ROOT, "theme", "img", "logo.png")
                )

            # Try each path until we find the logo
            logo_found = False
            for logo_path in possible_logo_paths:
                if os.path.exists(logo_path):
                    logo = Image(logo_path, width=150, height=45)
                    logo.hAlign = "CENTER"
                    elements.append(logo)
                    logo_found = True
                    break

            # If no logo is found, use a text title instead
            if not logo_found:
                elements.append(Paragraph("TechReform BD", title_style))
        except Exception as e:
            # If there's any issue with the logo, fall back to text
            print(f"Logo loading error: {str(e)}")
            elements.append(Paragraph("TechReform BD", title_style))

        # Add a separator line after logo
        elements.append(Spacer(1, 5 * mm))
        elements.append(
            HRFlowable(
                width="100%",
                thickness=1,
                color=tech_blue,
                spaceBefore=2 * mm,
                spaceAfter=5 * mm,
            )
        )

        # Add build title with date
        from datetime import datetime

        build_title = pc_build.name if pc_build.name else "Custom PC Build"
        current_date = datetime.now().strftime("%B %d, %Y")
        elements.append(Paragraph(build_title, title_style))
        elements.append(Paragraph(f"Generated on: {current_date}", normal_style))

        # Add total price with prominence
        total_price = pc_build.get_total_price
        elements.append(Paragraph(f"Total Price: {total_price:,.2f} Tk", price_style))
        elements.append(Spacer(1, 3 * mm))

        # Get all components by type for the component table
        table_data = [["Component", "Specification", "Price"]]

        components_data = []
        for item in pc_build.pcbuilderitem_set.all():
            if item.product_id:
                product = item.get_product()
                if product:
                    # Store component data for table
                    components_data.append(
                        {
                            "type": item.component_type,
                            "name": f"{product.brand} {product.model}",
                            "price": product.price,
                        }
                    )

        # Sort components in logical order
        component_order = [
            "CPU",
            "Cooler",
            "Motherboard",
            "RAM",
            "GPU",
            "SSD",
            "HDD",
            "Power Supply",
            "Casing",
            "Monitor",
            "Keyboard",
            "Mouse",
            "Headphone",
        ]

        # Add components to table in order
        for comp_type in component_order:
            for comp in components_data:
                if comp["type"] == comp_type:
                    # Wrap component names in Paragraph objects for text wrapping
                    name_paragraph = Paragraph(comp["name"], component_style)

                    table_data.append(
                        [
                            comp_type,
                            name_paragraph,
                            f"{comp['price']:,.2f} Tk" if comp["price"] else "N/A",
                        ]
                    )

        # Create the table with styling - adjusted column widths for text wrapping
        col_widths = [
            75,
            285,
            70,
        ]  # Width in points, with more space for component name
        components_table = Table(table_data, colWidths=col_widths, repeatRows=1)

        # Style the table with TechReform website colors
        table_style = TableStyle(
            [
                # Header row
                ("BACKGROUND", (0, 0), (-1, 0), tech_blue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                # Alternate row colors for better readability
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, tech_light_gray]),
                # Borders
                ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ("BOX", (0, 0), (-1, -1), 1, tech_light_blue),
                # Text alignment
                ("ALIGN", (0, 0), (0, -1), "LEFT"),  # Component type column
                ("ALIGN", (2, 0), (2, -1), "RIGHT"),  # Price column alignment
                ("VALIGN", (1, 1), (1, -1), "TOP"),  # Align wrapped text to top
                # Padding
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ]
        )

        components_table.setStyle(table_style)
        elements.append(Spacer(1, 5 * mm))
        elements.append(Paragraph("System Components", subtitle_style))
        elements.append(Spacer(1, 2 * mm))
        elements.append(components_table)
        elements.append(Spacer(1, 5 * mm))

        # Power consumption info box
        power_text = (
            f"<b>Estimated Power Consumption:</b> {pc_build.get_recommended_wattage}W"
        )
        elements.append(Paragraph(power_text, info_style))

        # System specifications
        elements.append(Paragraph("System Performance", subtitle_style))

        # Get components by type for detailed specs
        components_by_type = {}
        for item in pc_build.pcbuilderitem_set.all():
            if item.product_id:
                product = item.get_product()
                if product:
                    components_by_type[item.component_type] = product

        # Create specifications with detailed info
        specs_text = ""
        if "CPU" in components_by_type:
            cpu = components_by_type["CPU"]
            cpu_details = []
            if hasattr(cpu, "cores") and cpu.cores:
                cpu_details.append(f"{cpu.cores} cores")
            if hasattr(cpu, "threads") and cpu.threads:
                cpu_details.append(f"{cpu.threads} threads")
            if hasattr(cpu, "boost_frequency") and cpu.boost_frequency:
                cpu_details.append(f"{cpu.boost_frequency} GHz")
            cpu_specs = f"{cpu.brand} {cpu.model} " + (
                f"({', '.join(cpu_details)})" if cpu_details else ""
            )
            specs_text += f"<b>Processor:</b> {cpu_specs}<br/>"

        if "Cooler" in components_by_type:
            cooler = components_by_type["Cooler"]
            specs_text += f"<b>CPU Cooler:</b> {cooler.brand} {cooler.model}<br/>"

        if "Motherboard" in components_by_type:
            mobo = components_by_type["Motherboard"]
            mobo_details = []
            if hasattr(mobo, "chipset") and mobo.chipset:
                mobo_details.append(f"{mobo.chipset}")
            if hasattr(mobo, "form_factor") and mobo.form_factor:
                mobo_details.append(f"{mobo.form_factor}")
            mobo_specs = f"{mobo.brand} {mobo.model} " + (
                f"({', '.join(mobo_details)})" if mobo_details else ""
            )
            specs_text += f"<b>Motherboard:</b> {mobo_specs}<br/>"

        if "RAM" in components_by_type:
            ram = components_by_type["RAM"]
            ram_details = []
            if hasattr(ram, "memory_capacity") and ram.memory_capacity:
                ram_details.append(f"{ram.memory_capacity}")
            if hasattr(ram, "frequency") and ram.frequency:
                ram_details.append(f"{ram.frequency}")
            ram_specs = f"{ram.brand} {ram.model} " + (
                f"({', '.join(ram_details)})" if ram_details else ""
            )
            specs_text += f"<b>Memory:</b> {ram_specs}<br/>"

        if "GPU" in components_by_type:
            gpu = components_by_type["GPU"]
            gpu_details = []
            if hasattr(gpu, "vram_capacity") and gpu.vram_capacity:
                gpu_details.append(f"{gpu.vram_capacity}")
            gpu_specs = f"{gpu.brand} {gpu.model} " + (
                f"({', '.join(gpu_details)})" if gpu_details else ""
            )
            specs_text += f"<b>Graphics:</b> {gpu_specs}<br/>"

        storage_specs = []
        if "SSD" in components_by_type:
            ssd = components_by_type["SSD"]
            ssd_details = []
            if hasattr(ssd, "storage_capacity") and ssd.storage_capacity:
                ssd_details.append(f"{ssd.storage_capacity}")
            if hasattr(ssd, "interface") and ssd.interface:
                ssd_details.append(f"{ssd.interface}")
            ssd_specs = f"{ssd.brand} {ssd.model} " + (
                f"({', '.join(ssd_details)})" if ssd_details else ""
            )
            storage_specs.append(ssd_specs)

        if "HDD" in components_by_type:
            hdd = components_by_type["HDD"]
            hdd_details = []
            if hasattr(hdd, "storage_capacity") and hdd.storage_capacity:
                hdd_details.append(f"{hdd.storage_capacity}")
            if hasattr(hdd, "rpm") and hdd.rpm:
                hdd_details.append(f"{hdd.rpm}")
            hdd_specs = f"{hdd.brand} {hdd.model} " + (
                f"({', '.join(hdd_details)})" if hdd_details else ""
            )
            storage_specs.append(hdd_specs)

        if storage_specs:
            specs_text += f"<b>Storage:</b> {' + '.join(storage_specs)}<br/>"

        if "Power Supply" in components_by_type:
            psu = components_by_type["Power Supply"]
            psu_details = []
            if hasattr(psu, "wattage") and psu.wattage:
                psu_details.append(f"{psu.wattage}W")
            if hasattr(psu, "efficiency") and psu.efficiency:
                psu_details.append(f"{psu.efficiency}")
            psu_specs = f"{psu.brand} {psu.model} " + (
                f"({', '.join(psu_details)})" if psu_details else ""
            )
            specs_text += f"<b>Power Supply:</b> {psu_specs}<br/>"

        if "Casing" in components_by_type:
            case = components_by_type["Casing"]
            specs_text += f"<b>Case:</b> {case.brand} {case.model}<br/>"

        if specs_text:
            elements.append(Paragraph(specs_text, normal_style))

        # Compatibility Analysis
        elements.append(Paragraph("Compatibility Analysis", subtitle_style))

        # Check for compatibility issues
        compatibility_issues = []

        # CPU and Motherboard compatibility check
        cpu_item = pc_build.pcbuilderitem_set.filter(component_type="CPU").first()
        motherboard_item = pc_build.pcbuilderitem_set.filter(
            component_type="Motherboard"
        ).first()

        if (
            cpu_item
            and cpu_item.product_id
            and motherboard_item
            and motherboard_item.product_id
        ):
            cpu = cpu_item.get_product()
            motherboard = motherboard_item.get_product()

            if cpu and motherboard and cpu.socket != motherboard.socket:
                compatibility_issues.append(
                    f"⚠️ Socket mismatch: CPU uses {cpu.socket} but motherboard has {motherboard.socket}"
                )

        # RAM and Motherboard compatibility check
        ram_item = pc_build.pcbuilderitem_set.filter(component_type="RAM").first()
        if (
            ram_item
            and ram_item.product_id
            and motherboard_item
            and motherboard_item.product_id
        ):
            ram = ram_item.get_product()
            motherboard = motherboard_item.get_product()

            if ram and motherboard and ram.ram_type != motherboard.memory_type:
                compatibility_issues.append(
                    f"⚠️ Memory type mismatch: RAM is {ram.ram_type} but motherboard supports {motherboard.memory_type}"
                )

        # Case and Motherboard compatibility check
        case_item = pc_build.pcbuilderitem_set.filter(component_type="Casing").first()
        if (
            case_item
            and case_item.product_id
            and motherboard_item
            and motherboard_item.product_id
        ):
            case = case_item.get_product()
            motherboard = motherboard_item.get_product()

            if case and motherboard and motherboard.form_factor not in case.form_factor:
                compatibility_issues.append(
                    f"⚠️ Form factor mismatch: Motherboard is {motherboard.form_factor} but case supports {case.form_factor}"
                )

        # Power supply check
        power_item = pc_build.pcbuilderitem_set.filter(
            component_type="Power Supply"
        ).first()
        if power_item and power_item.product_id:
            power = power_item.get_product()
            recommended = pc_build.get_recommended_wattage

            if power.wattage < recommended:
                compatibility_issues.append(
                    f"⚠️ Insufficient power: Your build requires at least {recommended}W but your power supply provides {power.wattage}W"
                )

        # Display compatibility analysis
        if compatibility_issues:
            for issue in compatibility_issues:
                elements.append(Paragraph(issue, warning_style))
        else:
            elements.append(
                Paragraph("✅ All components are compatible.", compatible_style)
            )

        # Add recommendations section if there are missing components
        essential_components = ["CPU", "Motherboard", "RAM", "Power Supply", "Casing"]
        missing_essential = [
            comp for comp in essential_components if comp not in components_by_type
        ]

        if missing_essential:
            elements.append(Spacer(1, 5 * mm))
            elements.append(Paragraph("Build Recommendations", subtitle_style))
            recommendations = "To complete your build, consider adding the following essential components:<br/>"
            for missing in missing_essential:
                recommendations += f"• {missing}<br/>"
            elements.append(Paragraph(recommendations, normal_style))

        # Add a professional footer
        elements.append(Spacer(1, 10 * mm))
        elements.append(
            HRFlowable(
                width="100%",
                thickness=1,
                color=colors.lightgrey,
                spaceBefore=2 * mm,
                spaceAfter=5 * mm,
            )
        )
        current_year = datetime.now().year
        footer_text = f"© {current_year} TechReform BD • www.techreformbd.com • All prices valid at time of generation"
        elements.append(Paragraph(footer_text, footer_style))

        # Add page numbers
        def add_page_number(canvas, doc):
            canvas.saveState()
            canvas.setFont("Helvetica", 8)
            canvas.setFillColor(colors.grey)
            page_num = f"Page {canvas.getPageNumber()}"
            canvas.drawRightString(doc.pagesize[0] - 20 * mm, 15 * mm, page_num)
            canvas.restoreState()

        # Build the PDF with page numbers
        doc.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)

        # Get the PDF data
        pdf = buffer.getvalue()
        buffer.close()

        # Create response
        response = HttpResponse(content_type="application/pdf")
        filename = (
            pc_build.name.replace(" ", "_") if pc_build.name else "TechReform_PC_Build"
        )
        response["Content-Disposition"] = f'attachment; filename="{filename}.pdf"'
        response.write(pdf)

        return response

    except Exception as e:
        import traceback

        print(f"PDF Generation Error: {str(e)}")
        print(traceback.format_exc())  # Print detailed error for debugging
        messages.error(request, f"Error generating PDF: {str(e)}")
        return redirect("pc_builder")


def select_storage(request):
    """
    Display a unified storage component selection page combining SSD and HDD options.

    This specialized view provides a combined interface for selecting storage components,
    allowing users to browse both SSDs and HDDs in a single interface. It includes
    filtering by storage type, search functionality, and maintains the same
    compatibility and sorting features as other component selection pages.

    Args:
        request (HttpRequest): The HTTP request object containing query parameters.

    Returns:
        HttpResponse: Rendered storage selection page with combined SSD and HDD products.

    Query Parameters:
        search (str): Search term for filtering products by brand, model, or description
        sort (str): Sorting option ('price_asc', 'price_desc', 'name_asc', 'newest')
        compatibility_filter (str): If 'on', filters out incompatible products
        storage_type (str): Storage type filter ('all', 'ssd', 'hdd')
        page (int): Page number for pagination

    Product Processing:
        - Combines SSD and HDD models into unified product list
        - Adds storage_type attribute to distinguish between SSD and HDD
        - Applies stock status calculation (In Stock, Low Stock, Out of Stock)
        - Performs compatibility checking (storage is generally universal)
        - Supports search across both SSD and HDD models simultaneously

    Storage Type Filtering:
        - 'all': Shows both SSDs and HDDs (default)
        - 'ssd': Shows only SSD products
        - 'hdd': Shows only HDD products

    Context Variables:
        component_type (str): Set to 'Storage' for template compatibility
        products (Page): Paginated combined storage products
        search_query (str): Current search term
        current_sort (str): Current sorting option
        compatibility_filtered (bool): Whether compatibility filter is active
        storage_type (str): Current storage type filter
        current_selection (dict): Currently selected SSD and/or HDD components
        has_compatibility_check (bool): Whether compatibility checking is applicable

    Product Attributes Added:
        storage_type (str): 'SSD' or 'HDD' to distinguish product types
        stock_status (str): Stock availability status
        compatibility_issues (list): Any compatibility concerns (usually empty)
        is_compatible (bool): Compatibility status (usually True for storage)

    Template Considerations:
        - Uses same template as other component selection pages
        - Template must handle mixed product types (SSD and HDD)
        - Storage type is displayed to help users distinguish products
        - Supports filtering UI for storage type selection

    Notes:
        - Storage devices are generally compatible with most systems
        - No specific compatibility checks implemented (storage is universal)
        - Maintains consistency with other component selection interfaces
        - Supports both authenticated and anonymous users
        - Debug logging included for troubleshooting product queries
    """
    pc_build = get_or_create_pc_builder(request)

    # Get all selected components to determine compatibility
    selected_components = {}
    component_models = {
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

    for c_type in component_models.keys():
        try:
            item = PCBuilderItem.objects.get(pc_builder=pc_build, component_type=c_type)
            if item.product_id:
                selected_components[c_type] = item.get_product()
        except PCBuilderItem.DoesNotExist:
            pass

    # Get search query, sort choice, and compatibility filter preference
    search_query = request.GET.get("search", "")
    current_sort = request.GET.get("sort", "price_asc")
    compatibility_filtered = request.GET.get("compatibility_filter") == "on"

    # Specific filter for storage
    storage_type = request.GET.get("storage_type", "all")

    # Get products from both SSD and HDD models
    products = []

    # Debug information for console
    print(
        f"Storage selection - Query: {search_query}, Sort: {current_sort}, Storage type: {storage_type}"
    )

    # Get SSDs if not filtering to HDDs only
    if storage_type in ["all", "ssd"]:
        # Get all SSDs, don't filter by is_available
        ssd_queryset = SSD.objects.all()

        print(f"Found {ssd_queryset.count()} SSDs in database")

        # Apply search filter if provided
        if search_query:
            ssd_queryset = ssd_queryset.filter(
                Q(brand__icontains=search_query)
                | Q(model__icontains=search_query)
                | Q(description__icontains=search_query)
            )

        for ssd in ssd_queryset:
            # Make sure the storage type is marked
            ssd.storage_type = "SSD"
            products.append(ssd)

    # Get HDDs if not filtering to SSDs only
    if storage_type in ["all", "hdd"]:
        # Get all HDDs, don't filter by is_available
        hdd_queryset = HDD.objects.all()

        print(f"Found {hdd_queryset.count()} HDDs in database")

        # Apply search filter if provided
        if search_query:
            hdd_queryset = hdd_queryset.filter(
                Q(brand__icontains=search_query)
                | Q(model__icontains=search_query)
                | Q(description__icontains=search_query)
            )

        for hdd in hdd_queryset:
            # Make sure the storage type is marked
            hdd.storage_type = "HDD"
            products.append(hdd)

    print(f"Total combined storage products: {len(products)}")

    # Process all products
    for product in products:
        # Add stock status
        if product.stock > 10:
            product.stock_status = "In Stock"
        elif product.stock > 0:
            product.stock_status = "Low Stock"
        else:
            product.stock_status = "Out of Stock"

        # Initialize compatibility information
        product.compatibility_issues = []
        product.is_compatible = True  # Default to compatible

        # Add any storage-specific compatibility checks if needed
        # Storage devices are generally compatible with most systems

    # Apply sorting
    if current_sort == "price_asc":
        products = sorted(products, key=lambda x: x.price or 0)
    elif current_sort == "price_desc":
        products = sorted(products, key=lambda x: x.price or 0, reverse=True)
    elif current_sort == "name_asc":
        products = sorted(products, key=lambda x: f"{x.brand} {x.model}")
    elif current_sort == "newest":
        from datetime import datetime

        products = sorted(
            products,
            key=lambda x: x.created_at if hasattr(x, "created_at") else datetime.now(),
            reverse=True,
        )

    # Debug the first few products
    for i, p in enumerate(products[:5]):
        print(
            f"Product {i + 1}: {p.brand} {p.model} ({getattr(p, 'storage_type', 'Unknown')}) - Price: {p.price}"
        )

    # Get current SSD and HDD selections
    current_ssd = None
    current_hdd = None

    try:
        ssd_item = PCBuilderItem.objects.get(pc_builder=pc_build, component_type="SSD")
        if ssd_item.product_id:
            current_ssd = ssd_item.get_product()
    except PCBuilderItem.DoesNotExist:
        pass

    try:
        hdd_item = PCBuilderItem.objects.get(pc_builder=pc_build, component_type="HDD")
        if hdd_item.product_id:
            current_hdd = hdd_item.get_product()
    except PCBuilderItem.DoesNotExist:
        pass

    # Pagination
    paginator = Paginator(products, 12)  # 12 products per page
    page = request.GET.get("page", 1)

    try:
        products_page = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        products_page = paginator.page(1)

    context = {
        "component_type": "Storage",
        "products": products_page,
        "search_query": search_query,
        "current_sort": current_sort,
        "compatibility_filtered": compatibility_filtered,
        "storage_type": storage_type,
        "current_ssd": current_ssd,
        "current_hdd": current_hdd,
        "current_selection": current_ssd
        or current_hdd,  # For compatibility with the template
        "has_compatibility_check": bool(selected_components),
    }

    return render(request, "pcbuilder/pc-builder-select.html", context)
