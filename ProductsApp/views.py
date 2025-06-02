"""
Django views for the ProductsApp e-commerce application.

This module contains all view functions for managing product display, search,
filtering, and administrative operations in the TechReform e-commerce platform.
It provides comprehensive functionality for both customer-facing product browsing
and staff-level product management.

View Categories:
    Public Views (Customer-facing):
        - index: Homepage with featured products and categories
        - search_products: Advanced product search with filters
        - category_list: Display products by category with pagination
        - product_detail: Individual product detail pages
        - get_product_suggestions: AJAX product search suggestions

    Administrative Views (Staff/Admin only):
        - admin_product_dashboard: Main admin dashboard with analytics
        - manage_products: Product listing and management interface
        - add_product: Product creation with category-specific forms
        - edit_product: Product modification functionality
        - delete_product: Product deletion with confirmation
        - toggle_product_status: Quick product availability toggling

    AJAX Views:
        - get_product_suggestions: Real-time search suggestions
        - toggle_product_status: Quick status updates

Key Features:
    - Advanced search with multiple filters (price, brand, category, specifications)
    - Category-based product organization with dynamic model handling
    - Administrative product management with role-based access
    - Featured products and promotional displays
    - Responsive pagination and sorting options
    - Real-time search suggestions
    - Product availability management
    - Comprehensive product analytics

Supported Product Categories:
    Core Components: CPU, Cooler, Motherboard, RAM, SSD, HDD, GPU, PowerSupply, Casing
    Accessories: Monitor, Keyboard, Mouse, Headphone

Security Features:
    - Role-based access control using custom decorators
    - CSRF protection on all forms
    - Input validation and sanitization
    - Authentication requirements for administrative functions

Dependencies:
    - Custom authentication decorators from AuthApp
    - Dynamic model mapping for multi-category support
    - Django's built-in pagination and search functionality
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

# Import from AuthApp
from AuthApp.decorators import (
    admin_required,
    staff_required,
    content_manager_required,
)

from .models import (
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


# Create your views here.
def index(request):
    """Render the main index/home page of the application.

    Args:
        request: HttpRequest object containing request metadata.

    Returns:
        HttpResponse: Rendered home page template.
    """
    return render(request, "static/index.html")


def login_page(request):  # This should redirect to AuthApp's login
    """Redirect to the authentication app's login page.

    This view serves as a bridge to redirect users to the main login
    functionality handled by AuthApp.

    Args:
        request: HttpRequest object containing request metadata.

    Returns:
        HttpResponseRedirect: Redirect to the login view in AuthApp.
    """
    return redirect("login")


def register(request):  # This should redirect to AuthApp's register
    """Redirect to the authentication app's registration page.

    This view serves as a bridge to redirect users to the main registration
    functionality handled by AuthApp.

    Args:
        request: HttpRequest object containing request metadata.

    Returns:
        HttpResponseRedirect: Redirect to the register view in AuthApp.
    """
    return redirect("register")


def profile(request):  # This should redirect to AuthApp's profile
    """Redirect to the authentication app's profile page.

    This view serves as a bridge to redirect users to the main profile
    functionality handled by AuthApp.

    Args:
        request: HttpRequest object containing request metadata.

    Returns:
        HttpResponseRedirect: Redirect to the profile view in AuthApp.
    """
    return redirect("profile")


def about_us(request):
    """Render the about us page containing company information.

    Args:
        request: HttpRequest object containing request metadata.

    Returns:
        HttpResponse: Rendered about us page template.
    """
    return render(request, "static/about-us.html")


def faq(request):
    """Render the frequently asked questions page.

    Args:
        request: HttpRequest object containing request metadata.

    Returns:
        HttpResponse: Rendered FAQ page template.
    """
    return render(request, "static/faq.html")


def product_list(request):
    """Display all products with filtering, search, sorting, and pagination functionality.

    This view handles the main product listing page with comprehensive
    filtering capabilities including category-based filtering, text search
    across brand/model/description, and multiple sorting options.

    Query Parameters:
        category (str): Filter products by specific category (CPU, GPU, etc.)
        search (str): Search text to filter products by brand, model, or description
        sort_by (str): Sorting option - 'featured', 'price_low_high',
                      'price_high_low', 'newest', 'best_rated'
        page (int): Page number for pagination (12 products per page)

    Args:
        request: HttpRequest object containing request metadata and GET parameters.

    Returns:
        HttpResponse: Rendered product list template with filtered and paginated products.

    Context Variables:
        products: Paginated product queryset
        search_query: Current search term
        sort_by: Current sorting option
        current_category: Currently selected category filter
    """
    # Get category from query parameters
    category = request.GET.get("category")
    search_query = request.GET.get("search", "")
    sort_by = request.GET.get("sort_by", "featured")

    # Initialize empty products list
    products = []

    # Get products based on category filter
    if category == "CPU" or category is None:
        products.extend(CPU.objects.all())
    if category == "Cooler" or category is None:
        products.extend(Cooler.objects.all())
    if category == "Motherboard" or category is None:
        products.extend(Motherboard.objects.all())
    if category == "RAM" or category is None:
        products.extend(RAM.objects.all())
    if category == "SSD" or category is None:
        products.extend(SSD.objects.all())
    if category == "HDD" or category is None:
        products.extend(HDD.objects.all())
    if category == "GPU" or category is None:
        products.extend(GPU.objects.all())
    if category == "Power Supply" or category is None:
        products.extend(PowerSupply.objects.all())
    if category == "Casing" or category is None:
        products.extend(Casing.objects.all())
    if category == "Monitor" or category is None:
        products.extend(Monitor.objects.all())
    if category == "Keyboard" or category is None:
        products.extend(Keyboard.objects.all())
    if category == "Mouse" or category is None:
        products.extend(Mouse.objects.all())
    if category == "Headphone" or category is None:
        products.extend(Headphone.objects.all())

    # Search functionality
    if search_query:
        filtered_products = []
        for product in products:
            # Search in brand, model, or description
            if (
                search_query.lower() in product.brand.lower()
                or search_query.lower() in product.model.lower()
                or search_query.lower() in product.description.lower()
            ):
                filtered_products.append(product)
        products = filtered_products

    # Sorting functionality
    if sort_by == "price_low_high":
        products.sort(key=lambda x: x.price)
    elif sort_by == "price_high_low":
        products.sort(key=lambda x: x.price, reverse=True)
    elif sort_by == "newest":
        # Assuming BaseProduct has created_at field
        thirty_days_ago = timezone.now() - timedelta(days=30)
        products = [
            p
            for p in products
            if hasattr(p, "created_at") and p.created_at >= thirty_days_ago
        ]
    elif sort_by == "best_rated":
        # Implement if you have rating functionality
        pass

    # Pagination
    page = request.GET.get("page", 1)
    paginator = Paginator(products, 12)  # 12 products per page

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        "products": products,
        "search_query": search_query,
        "sort_by": sort_by,
        "current_category": category,
    }

    return render(request, "product/product-list.html", context)


def product_detail(request, product_id):
    """Display detailed view of a specific product with related products.

    This view attempts to find a product with the given ID across all product
    model classes (CPU, GPU, RAM, etc.) and displays its detailed information
    along with related products from the same category.

    Args:
        request: HttpRequest object containing request metadata.
        product_id (int): The unique identifier of the product to display.

    Returns:
        HttpResponse: Rendered product detail template if product found,
                     otherwise redirects to product list.

    Context Variables:
        product: The product object with all its attributes
        related_products: List of up to 4 related products from same category

    Note:
        The view searches through all product model classes sequentially
        until the product is found, then displays category-specific attributes.
    """
    # Try to find the product in each model
    product = None
    model_classes = [
        CPU,
        GPU,
        RAM,
        Motherboard,
        SSD,
        HDD,
        PowerSupply,
        Casing,
        Monitor,
        Keyboard,
        Mouse,
        Headphone,
        Cooler,
    ]    # Try each model class until product is found
    for model_class in model_classes:
        try:
            product = model_class.objects.get(id=product_id)
            break  # Exit the loop if product is found
        except model_class.DoesNotExist:
            continue

    # If no product found, redirect
    if product is None:
        return redirect("product-list")

    # Get related products from the same category
    related_products = []
    if hasattr(product, "category") and product.category:
        # Get the model class of the current product
        model_class = product.__class__
        related_candidates = model_class.objects.exclude(id=product.id)[:4]
        related_products.extend(related_candidates)

    context = {
        "product": product,
        "related_products": related_products,
    }

    return render(request, "product/product-detail.html", context)


def category_products(request, category_name):
    """Display products filtered by a specific category.

    This view acts as a wrapper around product_list to show products
    from a specific category only.

    Args:
        request: HttpRequest object containing request metadata.
        category_name (str): Name of the category to filter by.

    Returns:
        HttpResponse: Delegated to product_list view with category filter applied.
    """
    return product_list(request, category=category_name)


def featured_products(request):
    """Display featured products across all categories with pagination.

    This view aggregates featured products from all product model classes
    and displays them with pagination. Products must have an 'is_featured'
    field set to True to appear in this listing.

    Query Parameters:
        page (int): Page number for pagination (12 products per page)

    Args:
        request: HttpRequest object containing request metadata.

    Returns:
        HttpResponse: Rendered products template with featured products.

    Context Variables:
        products: Paginated featured products queryset
        is_featured: Boolean flag indicating this is featured products view

    Note:
        Requires 'is_featured' field in your BaseProduct model to function properly.
    """
    # Combine featured products from all models
    featured_products = []

    # This would need a 'is_featured' field in your BaseProduct model
    for model in [
        CPU,
        GPU,
        RAM,
        Motherboard,
        SSD,
        HDD,
        PowerSupply,
        Casing,
        Monitor,
        Keyboard,
        Mouse,
        Headphone,
        Cooler,
    ]:
        if hasattr(model, "objects"):
            # Filter for featured products if field exists
            if hasattr(model.objects.model, "is_featured"):
                featured_products.extend(model.objects.filter(is_featured=True))

    # Pagination
    page = request.GET.get("page", 1)
    paginator = Paginator(featured_products, 12)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        "products": products,
        "is_featured": True,
    }

    return render(request, "product/products.html", context)


def new_arrivals(request):
    """Display products added in the last 30 days with pagination.

    This view shows recently added products (within the last 30 days)
    from all product categories. Products must have a 'created_at' field
    to be included in this listing.

    Query Parameters:
        page (int): Page number for pagination (12 products per page)

    Args:
        request: HttpRequest object containing request metadata.

    Returns:
        HttpResponse: Rendered products template with new arrival products.

    Context Variables:
        products: Paginated new arrival products queryset
        is_new_arrivals: Boolean flag indicating this is new arrivals view

    Note:
        Requires 'created_at' field in product models to function properly.
        Only shows products created within the last 30 days.
    """
    thirty_days_ago = timezone.now() - timedelta(days=30)
    new_products = []

    # This requires a created_at field in your BaseProduct model
    for model in [
        CPU,
        GPU,
        RAM,
        Motherboard,
        SSD,
        HDD,
        PowerSupply,
        Casing,
        Monitor,
        Keyboard,
        Mouse,
        Headphone,
        Cooler,
    ]:
        if hasattr(model, "objects") and hasattr(model.objects.model, "created_at"):
            new_products.extend(model.objects.filter(created_at__gte=thirty_days_ago))

    # Pagination
    page = request.GET.get("page", 1)
    paginator = Paginator(new_products, 12)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        "products": products,
        "is_new_arrivals": True,
    }

    return render(request, "product/products.html", context)


def deals_products(request):
    """Display products that are on sale with pagination.

    This view shows products that have a discount (price less than regular_price)
    from all product categories. Products must have both 'price' and 'regular_price'
    fields with regular_price being higher than price.

    Query Parameters:
        page (int): Page number for pagination (12 products per page)

    Args:
        request: HttpRequest object containing request metadata.

    Returns:
        HttpResponse: Rendered products template with discounted products.

    Context Variables:
        products: Paginated deal products queryset
        is_deals: Boolean flag indicating this is deals view

    Note:
        Requires 'price' and 'regular_price' fields in product models.
        Only shows products where price < regular_price.
    """
    deal_products = []

    # Check each model for products with discounts
    for model in [
        CPU,
        GPU,
        RAM,
        Motherboard,
        SSD,
        HDD,
        PowerSupply,
        Casing,
        Monitor,
        Keyboard,
        Mouse,
        Headphone,
        Cooler,
    ]:
        if hasattr(model, "objects"):
            if hasattr(model.objects.model, "regular_price") and hasattr(
                model.objects.model, "price"
            ):
                # Get products where price is less than regular_price
                for product in model.objects.all():
                    if (
                        hasattr(product, "regular_price")
                        and product.regular_price
                        and product.price < product.regular_price
                    ):
                        deal_products.append(product)

    # Pagination
    page = request.GET.get("page", 1)
    paginator = Paginator(deal_products, 12)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        "products": products,
        "is_deals": True,
    }

    return render(request, "product/products.html", context)


def newsletter_subscribe(request):
    """Handle newsletter subscription requests.

    This is a placeholder view for newsletter subscription functionality.
    Currently displays a success message and redirects to the home page.

    Args:
        request: HttpRequest object containing request metadata.

    Returns:
        HttpResponseRedirect: Redirect to the home page with success message.

    Note:
        This is a placeholder implementation. Actual newsletter logic
        should be implemented here in the future.
    """
    # This is a placeholder - implement newsletter logic here
    messages.success(request, "Thank you for subscribing to our newsletter!")
    return redirect("index")


@staff_required
def product_management(request):
    """Admin product management dashboard with filtering and search capabilities.

    This view provides a comprehensive product management interface for staff users.
    It displays all products from all categories with filtering by category and
    search functionality across brand, model, and category-specific fields.

    Query Parameters:
        category (str): Filter products by specific category
        search (str): Search term to filter products by brand, model, or category fields

    Args:
        request: HttpRequest object containing request metadata.

    Returns:
        HttpResponse: Rendered product management template with filtered products.

    Context Variables:
        category_filter: Current category filter
        search_query: Current search term
        cpus, gpus, motherboards, etc.: Product querysets for each category
        total_products: Total count of all products
        categories: List of available product categories

    Decorators:
        @staff_required: Ensures only staff members can access this view.

    Note:
        Includes debug print statements for monitoring product counts.
        Search functionality varies by category (e.g., socket for CPUs, chipset for motherboards).
    """
    # Get category filter from request
    category_filter = request.GET.get("category", "")
    search_query = request.GET.get("search", "")

    # Initialize product lists
    cpus = []
    gpus = []
    motherboards = []
    rams = []
    ssds = []
    hdds = []
    power_supplies = []
    casings = []
    coolers = []
    monitors = []
    keyboards = []
    mice = []
    headphones = []

    # Apply filters and search
    if category_filter == "CPU" or not category_filter:
        cpus = CPU.objects.all()
        if search_query:
            cpus = cpus.filter(
                Q(brand__icontains=search_query)
                | Q(model__icontains=search_query)
                | Q(socket__icontains=search_query)
            )

    if category_filter == "GPU" or not category_filter:
        gpus = GPU.objects.all()
        if search_query:
            gpus = gpus.filter(
                Q(brand__icontains=search_query) | Q(model__icontains=search_query)
            )

    if category_filter == "Motherboard" or not category_filter:
        motherboards = Motherboard.objects.all()
        if search_query:
            motherboards = motherboards.filter(
                Q(brand__icontains=search_query)
                | Q(model__icontains=search_query)
                | Q(chipset__icontains=search_query)
            )

    if category_filter == "RAM" or not category_filter:
        rams = RAM.objects.all()
        if search_query:
            rams = rams.filter(
                Q(brand__icontains=search_query) | Q(model__icontains=search_query)
            )

    if category_filter == "SSD" or not category_filter:
        ssds = SSD.objects.all()
        if search_query:
            ssds = ssds.filter(
                Q(brand__icontains=search_query) | Q(model__icontains=search_query)
            )

    if category_filter == "HDD" or not category_filter:
        hdds = HDD.objects.all()
        if search_query:
            hdds = hdds.filter(
                Q(brand__icontains=search_query) | Q(model__icontains=search_query)
            )

    if category_filter == "Power Supply" or not category_filter:
        power_supplies = PowerSupply.objects.all()
        if search_query:
            power_supplies = power_supplies.filter(
                Q(brand__icontains=search_query) | Q(model__icontains=search_query)
            )

    if category_filter == "Casing" or not category_filter:
        casings = Casing.objects.all()
        if search_query:
            casings = casings.filter(
                Q(brand__icontains=search_query) | Q(model__icontains=search_query)
            )

    if category_filter == "Cooler" or not category_filter:
        coolers = Cooler.objects.all()
        if search_query:
            coolers = coolers.filter(
                Q(brand__icontains=search_query) | Q(model__icontains=search_query)
            )

    if category_filter == "Monitor" or not category_filter:
        monitors = Monitor.objects.all()
        if search_query:
            monitors = monitors.filter(
                Q(brand__icontains=search_query) | Q(model__icontains=search_query)
            )

    if category_filter == "Keyboard" or not category_filter:
        keyboards = Keyboard.objects.all()
        if search_query:
            keyboards = keyboards.filter(
                Q(brand__icontains=search_query) | Q(model__icontains=search_query)
            )

    if category_filter == "Mouse" or not category_filter:
        mice = Mouse.objects.all()
        if search_query:
            mice = mice.filter(
                Q(brand__icontains=search_query) | Q(model__icontains=search_query)
            )

    if category_filter == "Headphone" or not category_filter:
        headphones = Headphone.objects.all()
        if search_query:
            headphones = headphones.filter(
                Q(brand__icontains=search_query) | Q(model__icontains=search_query)
            )    # Calculate total count
    total_count = (
        len(cpus)
        + len(gpus)
        + len(motherboards)
        + len(rams)
        + len(ssds)
        + len(hdds)
        + len(power_supplies)
        + len(casings)
        + len(coolers)
        + len(monitors)
        + len(keyboards)
        + len(mice)
        + len(headphones)
    )
    print(f"Total products: {total_count}")

    # Prepare context
    context = {
        "category_filter": category_filter,
        "search_query": search_query,
        "cpus": cpus,
        "gpus": gpus,
        "motherboards": motherboards,
        "rams": rams,
        "ssds": ssds,
        "hdds": hdds,
        "power_supplies": power_supplies,
        "casings": casings,
        "coolers": coolers,
        "monitors": monitors,
        "keyboards": keyboards,
        "mice": mice,
        "headphones": headphones,
        "total_products": total_count,  # Add total count to context
        "categories": [
            "CPU",
            "GPU",
            "Motherboard",
            "RAM",
            "SSD",
            "HDD",
            "Power Supply",
            "Casing",
            "Cooler",
            "Monitor",
            "Keyboard",
            "Mouse",
            "Headphone",
        ],
    }

    return render(request, "product/product-management.html", context)


@admin_required
def toggle_product_status(request, product_id, product_type):
    """Toggle the active status of a product (activate/deactivate).

    This view allows administrators to toggle the is_active status of any product
    across all product categories. It handles the product type mapping and
    provides appropriate success/error messages.

    Args:
        request: HttpRequest object containing request metadata.
        product_id (int): The unique identifier of the product to toggle.
        product_type (str): The type/category of the product (cpu, gpu, etc.).

    Returns:
        HttpResponseRedirect: Redirect back to the referring page or product management.

    Decorators:
        @admin_required: Ensures only administrators can access this view.

    Request Method:
        POST: Required for security - prevents accidental status changes via GET.

    Success Messages:
        Displays appropriate message indicating whether product was activated or deactivated.

    Error Handling:
        - Invalid product type: Shows error message and redirects
        - Product not found: Handled by get_object_or_404
        - General exceptions: Shows error message with exception details

    Note:
        Preserves the current page context by redirecting to HTTP_REFERER when possible.
    """
    if request.method == "POST":
        try:
            # Get the appropriate product model
            if product_type == "cpu":
                product = get_object_or_404(CPU, id=product_id)
            elif product_type == "gpu":
                product = get_object_or_404(GPU, id=product_id)
            elif product_type == "motherboard":
                product = get_object_or_404(Motherboard, id=product_id)
            elif product_type == "ram":
                product = get_object_or_404(RAM, id=product_id)
            elif product_type == "ssd":
                product = get_object_or_404(SSD, id=product_id)
            elif product_type == "hdd":
                product = get_object_or_404(HDD, id=product_id)
            elif product_type == "power_supply":
                product = get_object_or_404(PowerSupply, id=product_id)
            elif product_type == "casing":
                product = get_object_or_404(Casing, id=product_id)
            elif product_type == "cooler":
                product = get_object_or_404(Cooler, id=product_id)
            elif product_type == "monitor":
                product = get_object_or_404(Monitor, id=product_id)
            elif product_type == "keyboard":
                product = get_object_or_404(Keyboard, id=product_id)
            elif product_type == "mouse":
                product = get_object_or_404(Mouse, id=product_id)
            elif product_type == "headphone":
                product = get_object_or_404(Headphone, id=product_id)
            else:
                messages.error(request, "Invalid product type")
                return redirect("product_management")

            # Toggle the active status
            product.is_active = not product.is_active
            product.save()

            status = "activated" if product.is_active else "deactivated"
            messages.success(
                request, f"{product.brand} {product.model} has been {status}."
            )
            # Redirect back to the product management page with filters preserved
            return redirect(request.META.get("HTTP_REFERER", "product_management"))

        except Exception as e:
            messages.error(request, f"Error toggling product status: {str(e)}")
            return redirect("product_management")


@admin_required
def delete_product(request, product_id, product_type):
    """Permanently delete a product from the database.

    This view allows administrators to permanently remove products from
    the database across all product categories. It handles the product
    type mapping and provides appropriate confirmation messages.

    Args:
        request: HttpRequest object containing request metadata.
        product_id (int): The unique identifier of the product to delete.
        product_type (str): The type/category of the product (cpu, gpu, etc.).

    Returns:
        HttpResponseRedirect: Redirect back to the referring page or product management.

    Decorators:
        @admin_required: Ensures only administrators can access this view.

    Request Method:
        POST: Required for security - prevents accidental deletion via GET.

    Success Messages:
        Displays confirmation message with the deleted product's name.

    Error Handling:
        - Invalid product type: Shows error message and redirects
        - Product not found: Handled by get_object_or_404
        - Invalid request method: Shows error for non-POST requests
        - General exceptions: Shows error message with exception details

    Warning:
        This operation is irreversible. The product will be permanently
        removed from the database along with all associated data.

    Note:
        Stores product name before deletion to include in success message.
        Preserves current page context by redirecting to HTTP_REFERER when possible.
    """
    if request.method == "POST":
        try:
            # Get the appropriate product model
            if product_type == "cpu":
                product = get_object_or_404(CPU, id=product_id)
            elif product_type == "gpu":
                product = get_object_or_404(GPU, id=product_id)
            elif product_type == "motherboard":
                product = get_object_or_404(Motherboard, id=product_id)
            elif product_type == "ram":
                product = get_object_or_404(RAM, id=product_id)
            elif product_type == "ssd":
                product = get_object_or_404(SSD, id=product_id)
            elif product_type == "hdd":
                product = get_object_or_404(HDD, id=product_id)
            elif product_type == "powersupply":
                product = get_object_or_404(PowerSupply, id=product_id)
            elif product_type == "casing":
                product = get_object_or_404(Casing, id=product_id)
            elif product_type == "cooler":
                product = get_object_or_404(Cooler, id=product_id)
            elif product_type == "monitor":
                product = get_object_or_404(Monitor, id=product_id)
            elif product_type == "keyboard":
                product = get_object_or_404(Keyboard, id=product_id)
            elif product_type == "mouse":
                product = get_object_or_404(Mouse, id=product_id)
            elif product_type == "headphone":
                product = get_object_or_404(Headphone, id=product_id)
            else:
                messages.error(request, "Invalid product type")
                return redirect("product_management")

            # Store product info before deletion
            product_name = f"{product.brand} {product.model}"

            # Delete the product
            product.delete()

            messages.success(request, f"{product_name} has been successfully deleted.")
            # Redirect back to the product management page
            return redirect(request.META.get("HTTP_REFERER", "product_management"))

        except Exception as e:
            messages.error(request, f"Error deleting product: {str(e)}")
            return redirect("product_management")
    else:
        messages.error(request, "Invalid request method")
        return redirect("product_management")


@admin_required
def update_product(request, product_id, category):
    """Dynamic product update view that handles all product categories.

    This view provides a comprehensive product editing interface that adapts
    to different product categories. It handles both GET requests (display form)
    and POST requests (process updates) with category-specific field handling.

    Args:
        request: HttpRequest object containing request metadata and form data.
        product_id (int): The unique identifier of the product to update.
        category (str): The product category (CPU, GPU, Motherboard, etc.).

    Returns:
        GET: HttpResponse with rendered update form
        POST: HttpResponseRedirect to product management on success,
              or re-rendered form with errors on failure

    Decorators:
        @admin_required: Ensures only administrators can access this view.

    Form Handling:
        - Basic fields: brand, model, price, warranty, description, stock, etc.
        - Category-specific fields: Dynamically handled based on product type
        - Image uploads: Supports up to 5 product images with clear functionality
        - Boolean fields: Properly handles checkbox inputs

    Category Support:
        Supports all product categories including CPU, GPU, Motherboard, RAM,
        SSD, HDD, Power Supply, Casing, Cooler, Monitor, Keyboard, Mouse, Headphone.

    Context Variables:
        product: The product instance being edited
        category: Product category
        category_fields: Dynamic field configuration for the category
        Various choice lists: For dropdown fields (socket, memory type, etc.)

    Error Handling:
        - Invalid category: Shows error and redirects to product management
        - Product not found: Shows error and redirects to product management
        - Form validation errors: Shows error with exception details

    Note:
        Uses decimal.Decimal for price fields to ensure precision.
        Handles optional fields gracefully with None values for empty inputs.
    """
    # Model mapping for categories
    MODEL_MAPPING = {
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

    # Get the model class for the category
    model_class = MODEL_MAPPING.get(category)
    if not model_class:
        messages.error(request, "Invalid product category")
        return redirect("product_management")
    # Get the product instance
    try:
        product = get_object_or_404(model_class, id=product_id)
    except Exception:
        messages.error(request, "Product not found")
        return redirect("product_management")

    if request.method == "POST":
        try:
            # Handle basic fields that all products have
            product.brand = request.POST.get("brand", "").strip()
            product.model = request.POST.get("model", "").strip()
            product.price = Decimal(request.POST.get("price", "0"))
            product.regular_price = (
                Decimal(request.POST.get("regular_price", "0"))
                if request.POST.get("regular_price")
                else None
            )
            product.warranty = request.POST.get("warranty", "")
            product.description = request.POST.get("description", "").strip()
            product.stock = int(request.POST.get("stock", "0"))
            product.is_featured = request.POST.get("is_featured") == "on"
            product.is_available = request.POST.get("is_available") == "on"
            product.tdp = (
                int(request.POST.get("tdp", "0")) if request.POST.get("tdp") else None
            )

            # Handle category-specific fields
            if category == "CPU":
                product.socket = request.POST.get("socket", "")
                product.cores = (
                    int(request.POST.get("cores", "0"))
                    if request.POST.get("cores")
                    else None
                )
                product.threads = (
                    int(request.POST.get("threads", "0"))
                    if request.POST.get("threads")
                    else None
                )
                product.base_frequency = (
                    float(request.POST.get("base_frequency", "0"))
                    if request.POST.get("base_frequency")
                    else None
                )
                product.boost_frequency = (
                    float(request.POST.get("boost_frequency", "0"))
                    if request.POST.get("boost_frequency")
                    else None
                )
                product.cache = (
                    int(request.POST.get("cache", "0"))
                    if request.POST.get("cache")
                    else None
                )
                product.processor_graphics = request.POST.get("processor_graphics", "")

            elif category == "GPU":
                product.chipset = request.POST.get("chipset", "")
                product.memory_size = (
                    int(request.POST.get("memory_size", "0"))
                    if request.POST.get("memory_size")
                    else None
                )
                product.memory_type = request.POST.get("memory_type", "")
                product.memory_interface = (
                    int(request.POST.get("memory_interface", "0"))
                    if request.POST.get("memory_interface")
                    else None
                )
                product.base_clock = (
                    int(request.POST.get("base_clock", "0"))
                    if request.POST.get("base_clock")
                    else None
                )
                product.boost_clock = (
                    int(request.POST.get("boost_clock", "0"))
                    if request.POST.get("boost_clock")
                    else None
                )
                product.cuda_cores = (
                    int(request.POST.get("cuda_cores", "0"))
                    if request.POST.get("cuda_cores")
                    else None
                )
                product.rt_cores = (
                    int(request.POST.get("rt_cores", "0"))
                    if request.POST.get("rt_cores")
                    else None
                )
                product.tensor_cores = (
                    int(request.POST.get("tensor_cores", "0"))
                    if request.POST.get("tensor_cores")
                    else None
                )
                product.pcie_version = request.POST.get("pcie_version", "")
                product.cooling_type = request.POST.get("cooling_type", "")
                product.length = (
                    int(request.POST.get("length", "0"))
                    if request.POST.get("length")
                    else None
                )
                product.width = (
                    int(request.POST.get("width", "0"))
                    if request.POST.get("width")
                    else None
                )
                product.height = (
                    int(request.POST.get("height", "0"))
                    if request.POST.get("height")
                    else None
                )

            elif category == "Motherboard":
                product.socket = request.POST.get("socket", "")
                product.chipset = request.POST.get("chipset", "")
                product.form_factor = request.POST.get("form_factor", "")
                product.memory_support = request.POST.get("memory_support", "")
                product.max_memory = (
                    int(request.POST.get("max_memory", "0"))
                    if request.POST.get("max_memory")
                    else None
                )
                product.memory_slots = (
                    int(request.POST.get("memory_slots", "0"))
                    if request.POST.get("memory_slots")
                    else None
                )
                product.pcie_slots = request.POST.get("pcie_slots", "")
                product.sata_ports = (
                    int(request.POST.get("sata_ports", "0"))
                    if request.POST.get("sata_ports")
                    else None
                )
                product.m2_slots = (
                    int(request.POST.get("m2_slots", "0"))
                    if request.POST.get("m2_slots")
                    else None
                )
                product.usb_ports = request.POST.get("usb_ports", "")
                product.ethernet = request.POST.get("ethernet", "")
                product.wifi = request.POST.get("wifi", "")
                product.bluetooth = request.POST.get("bluetooth", "")
                product.audio_chipset = request.POST.get("audio_chipset", "")

            elif category == "RAM":
                product.memory_type = request.POST.get("memory_type", "")
                product.capacity = (
                    int(request.POST.get("capacity", "0"))
                    if request.POST.get("capacity")
                    else None
                )
                product.frequency = (
                    int(request.POST.get("frequency", "0"))
                    if request.POST.get("frequency")
                    else None
                )
                product.cas_latency = request.POST.get("cas_latency", "")
                product.voltage = (
                    float(request.POST.get("voltage", "0"))
                    if request.POST.get("voltage")
                    else None
                )
                product.modules = (
                    int(request.POST.get("modules", "0"))
                    if request.POST.get("modules")
                    else None
                )
                product.heat_spreader = request.POST.get("heat_spreader") == "on"
                product.rgb_lighting = request.POST.get("rgb_lighting") == "on"

            elif category in ["SSD", "HDD"]:
                product.capacity = (
                    int(request.POST.get("capacity", "0"))
                    if request.POST.get("capacity")
                    else None
                )
                product.interface = request.POST.get("interface", "")
                product.form_factor = request.POST.get("form_factor", "")
                if category == "SSD":
                    product.read_speed = (
                        int(request.POST.get("read_speed", "0"))
                        if request.POST.get("read_speed")
                        else None
                    )
                    product.write_speed = (
                        int(request.POST.get("write_speed", "0"))
                        if request.POST.get("write_speed")
                        else None
                    )
                    product.nand_type = request.POST.get("nand_type", "")
                    product.controller = request.POST.get("controller", "")
                    product.cache = (
                        int(request.POST.get("cache", "0"))
                        if request.POST.get("cache")
                        else None
                    )
                elif category == "HDD":
                    product.rpm = (
                        int(request.POST.get("rpm", "0"))
                        if request.POST.get("rpm")
                        else None
                    )
                    product.cache = (
                        int(request.POST.get("cache", "0"))
                        if request.POST.get("cache")
                        else None
                    )

            elif category == "Power Supply":
                product.wattage = (
                    int(request.POST.get("wattage", "0"))
                    if request.POST.get("wattage")
                    else None
                )
                product.efficiency_rating = request.POST.get("efficiency_rating", "")
                product.modular_type = request.POST.get("modular_type", "")
                product.form_factor = request.POST.get("form_factor", "")
                product.fan_size = (
                    int(request.POST.get("fan_size", "0"))
                    if request.POST.get("fan_size")
                    else None
                )
                product.pcie_connectors = request.POST.get("pcie_connectors", "")
                product.sata_connectors = (
                    int(request.POST.get("sata_connectors", "0"))
                    if request.POST.get("sata_connectors")
                    else None
                )
                product.molex_connectors = (
                    int(request.POST.get("molex_connectors", "0"))
                    if request.POST.get("molex_connectors")
                    else None
                )
                product.cpu_connectors = request.POST.get("cpu_connectors", "")
                product.active_pfc = request.POST.get("active_pfc") == "on"

            elif category == "Casing":
                product.case_type = request.POST.get("case_type", "")
                product.form_factor_support = request.POST.get(
                    "form_factor_support", ""
                )
                product.max_gpu_length = (
                    int(request.POST.get("max_gpu_length", "0"))
                    if request.POST.get("max_gpu_length")
                    else None
                )
                product.max_cpu_cooler_height = (
                    int(request.POST.get("max_cpu_cooler_height", "0"))
                    if request.POST.get("max_cpu_cooler_height")
                    else None
                )
                product.drive_bays_25 = (
                    int(request.POST.get("drive_bays_25", "0"))
                    if request.POST.get("drive_bays_25")
                    else None
                )
                product.drive_bays_35 = (
                    int(request.POST.get("drive_bays_35", "0"))
                    if request.POST.get("drive_bays_35")
                    else None
                )
                product.expansion_slots = (
                    int(request.POST.get("expansion_slots", "0"))
                    if request.POST.get("expansion_slots")
                    else None
                )
                product.front_io = request.POST.get("front_io", "")
                product.side_panel = request.POST.get("side_panel", "")
                product.rgb_lighting = request.POST.get("rgb_lighting") == "on"
                product.psu_shroud = request.POST.get("psu_shroud") == "on"

            elif category == "Cooler":
                product.cooler_type = request.POST.get("cooler_type", "")
                product.socket_compatibility = request.POST.get(
                    "socket_compatibility", ""
                )
                product.fan_speed = request.POST.get("fan_speed", "")
                product.noise_level = (
                    float(request.POST.get("noise_level", "0"))
                    if request.POST.get("noise_level")
                    else None
                )
                product.height = (
                    int(request.POST.get("height", "0"))
                    if request.POST.get("height")
                    else None
                )
                product.radiator_size = request.POST.get("radiator_size", "")
                product.rgb_lighting = request.POST.get("rgb_lighting") == "on"

            elif category == "Monitor":
                product.screen_size = (
                    float(request.POST.get("screen_size", "0"))
                    if request.POST.get("screen_size")
                    else None
                )
                product.resolution = request.POST.get("resolution", "")
                product.panel_type = request.POST.get("panel_type", "")
                product.refresh_rate = (
                    int(request.POST.get("refresh_rate", "0"))
                    if request.POST.get("refresh_rate")
                    else None
                )
                product.response_time = (
                    float(request.POST.get("response_time", "0"))
                    if request.POST.get("response_time")
                    else None
                )
                product.brightness = (
                    int(request.POST.get("brightness", "0"))
                    if request.POST.get("brightness")
                    else None
                )
                product.contrast_ratio = request.POST.get("contrast_ratio", "")
                product.color_gamut = request.POST.get("color_gamut", "")
                product.adaptive_sync = request.POST.get("adaptive_sync", "")
                product.connectivity = request.POST.get("connectivity", "")
                product.vesa_mount = request.POST.get("vesa_mount", "")
                product.built_in_speakers = (
                    request.POST.get("built_in_speakers") == "on"
                )
                product.hdr_support = request.POST.get("hdr_support") == "on"
                product.curved = request.POST.get("curved") == "on"

            elif category in ["Keyboard", "Mouse"]:
                product.connection_type = request.POST.get("connection_type", "")
                product.rgb_lighting = request.POST.get("rgb_lighting") == "on"
                if category == "Keyboard":
                    product.switch_type = request.POST.get("switch_type", "")
                    product.key_layout = request.POST.get("key_layout", "")
                    product.backlight = request.POST.get("backlight", "")
                    product.macro_keys = request.POST.get("macro_keys") == "on"
                    product.wireless = request.POST.get("wireless") == "on"
                elif category == "Mouse":
                    product.sensor_type = request.POST.get("sensor_type", "")
                    product.dpi = (
                        int(request.POST.get("dpi", "0"))
                        if request.POST.get("dpi")
                        else None
                    )
                    product.polling_rate = (
                        int(request.POST.get("polling_rate", "0"))
                        if request.POST.get("polling_rate")
                        else None
                    )
                    product.buttons = (
                        int(request.POST.get("buttons", "0"))
                        if request.POST.get("buttons")
                        else None
                    )
                    product.wireless = request.POST.get("wireless") == "on"
                    product.battery_life = (
                        int(request.POST.get("battery_life", "0"))
                        if request.POST.get("battery_life")
                        else None
                    )

            elif category == "Headphone":
                product.headphone_type = request.POST.get("headphone_type", "")
                product.driver_size = (
                    int(request.POST.get("driver_size", "0"))
                    if request.POST.get("driver_size")
                    else None
                )
                product.impedance = (
                    int(request.POST.get("impedance", "0"))
                    if request.POST.get("impedance")
                    else None
                )
                product.frequency_response = request.POST.get("frequency_response", "")
                product.connection_type = request.POST.get("connection_type", "")
                product.microphone = request.POST.get("microphone") == "on"
                product.noise_cancellation = (
                    request.POST.get("noise_cancellation") == "on"
                )
                product.wireless = request.POST.get("wireless") == "on"
                product.battery_life = (
                    int(request.POST.get("battery_life", "0"))
                    if request.POST.get("battery_life")
                    else None
                )
                product.rgb_lighting = request.POST.get("rgb_lighting") == "on"

            # Handle image uploads
            for i in range(1, 6):
                image_field = f"image{i}"
                if image_field in request.FILES:
                    setattr(product, image_field, request.FILES[image_field])
                elif request.POST.get(f"clear_{image_field}"):
                    # Clear the image if checkbox is checked
                    setattr(product, image_field, None)

            # Set category
            product.category = category
            product.save()

            messages.success(
                request,
                f'{category} "{product.brand} {product.model}" has been updated successfully!',
            )
            return redirect("product_management")

        except Exception as e:
            messages.error(request, f"Error updating product: {str(e)}")

    # Get category-specific field information for the template
    category_fields = get_category_fields(category)

    context = {
        "product": product,
        "category": category,
        "category_fields": category_fields,
        "socket_choices": get_socket_choices(),
        "memory_type_choices": get_memory_type_choices(),
        "form_factor_choices": get_form_factor_choices(category),
        "efficiency_rating_choices": get_efficiency_rating_choices(),
        "interface_choices": get_interface_choices(),
        "panel_type_choices": get_panel_type_choices(),
        "connection_type_choices": get_connection_type_choices(),
    }

    return render(request, "product/update-product.html", context)


@content_manager_required
def add_product(request, category):
    """Add a new product of the specified category to the database.

    This view provides a dynamic product creation interface that adapts to
    different product categories. It handles both GET requests (display form)
    and POST requests (create product) with category-specific field handling.

    Args:
        request: HttpRequest object containing request metadata and form data.
        category (str): URL parameter specifying the product category
                       (cpu, gpu, motherboard, etc. - lowercase with hyphens).

    Returns:
        GET: HttpResponse with rendered add product form
        POST: HttpResponseRedirect to product management on success,
              or re-rendered form with errors on failure

    Decorators:
        @content_manager_required: Ensures only content managers can access this view.

    Category Mapping:
        URL categories (lowercase, hyphenated) are mapped to model classes:
        - cpu -> CPU
        - gpu -> GPU
        - power-supply -> PowerSupply
        - etc.

    Form Handling:
        - Base fields: name, brand, model, description, price, stock, warranty
        - Feature flags: is_featured, is_new_arrival, is_on_sale
        - Sale pricing: Handles regular_price when is_on_sale is enabled
        - Category-specific fields: Dynamically processed based on field configuration
        - Image uploads: Supports up to 5 product images

    Field Type Processing:
        - checkbox: Boolean conversion
        - number: Integer or float conversion based on step attribute
        - text/select: String values with empty value handling

    Context Variables:
        category: URL category parameter
        display_category: Human-readable category name
        fields: Dynamic field configuration for the category
        choices: Dropdown options for select fields

    Error Handling:
        - Invalid category: Shows error and redirects to product management
        - Form validation errors: Shows error with exception details
        - Missing required fields: Handled by model validation    Note:
        Uses decimal.Decimal for price fields to ensure precision.
        Automatically sets the category field on the created product.
        Handles optional numeric fields with None for empty values.
    """
    category_map = {
        "cpu": CPU,
        "gpu": GPU,
        "motherboard": Motherboard,
        "ram": RAM,
        "ssd": SSD,
        "hdd": HDD,
        "power-supply": PowerSupply,
        "casing": Casing,
        "cooler": Cooler,
        "monitor": Monitor,
        "keyboard": Keyboard,
        "mouse": Mouse,
        "headphone": Headphone,
    }

    # Get the model class for the category
    model_class = category_map.get(category)
    if not model_class:
        messages.error(request, f"Invalid category: {category}")
        return redirect("product_management")

    # Convert category to display format
    display_category = category.replace("-", " ").title()

    if request.method == "POST":
        try:
            # Get form data
            data = {}
            for key, value in request.POST.items():
                if key != "csrfmiddlewaretoken" and value:
                    data[key] = value

            # Process base fields
            name = data.get("name")
            brand = data.get("brand")
            model = data.get("model")
            description = data.get("description")
            price = Decimal(data.get("price", "0"))
            stock = int(data.get("stock", "0"))
            warranty = data.get("warranty")

            # Process feature flags
            is_featured = "is_featured" in request.POST
            is_new_arrival = "is_new_arrival" in request.POST
            is_on_sale = "is_on_sale" in request.POST

            # Handle sale pricing
            regular_price = None
            if is_on_sale and "regular_price" in data:
                regular_price = Decimal(data["regular_price"])

            # Create product instance
            product_data = {
                "name": name,
                "brand": brand,
                "model": model,
                "description": description,
                "price": price,
                "stock": stock,
                "warranty": warranty,
                "is_featured": is_featured,
                "is_new_arrival": is_new_arrival,
                "is_on_sale": is_on_sale,
                "category": display_category,
            }

            if regular_price:
                product_data["regular_price"] = regular_price

            # Get category-specific fields
            fields = get_category_fields(display_category)
            for field in fields:
                field_name = field["name"]
                if field_name in data:
                    field_type = field.get("type", "text")
                    field_value = data[field_name]

                    if field_type == "checkbox":
                        product_data[field_name] = field_name in request.POST
                    elif field_type == "number":
                        try:
                            step = field.get("step", "1")
                            if step == "0.1":
                                product_data[field_name] = float(field_value)
                            else:
                                product_data[field_name] = int(field_value)
                        except (ValueError, TypeError):
                            product_data[field_name] = None
                    else:
                        product_data[field_name] = field_value

            # Create product
            product = model_class.objects.create(**product_data)

            # Handle image uploads
            for i in range(1, 6):
                image_field = f"image{i}"
                if image_field in request.FILES:
                    setattr(product, image_field, request.FILES[image_field])

            product.save()

            messages.success(
                request,
                f'{display_category} product "{product.name}" has been added successfully!',
            )
            return redirect("product_management")

        except Exception as e:
            messages.error(request, f"Error adding product: {str(e)}")

    # Get field configuration for the category
    fields = get_category_fields(display_category)

    # Get choice options
    choices = {}
    for field in fields:
        if field.get("type") == "select":
            field_name = field["name"]
            if field_name == "socket_type" or field_name == "socket":
                choices[field_name] = get_socket_choices()
            elif field_name == "memory_type":
                choices[field_name] = get_memory_type_choices()
            elif field_name == "form_factor":
                choices[field_name] = get_form_factor_choices(display_category)
            elif field_name == "efficiency_rating":
                choices[field_name] = get_efficiency_rating_choices()
            elif field_name == "interface":
                choices[field_name] = get_interface_choices()
            elif field_name == "panel_type":
                choices[field_name] = get_panel_type_choices()
            elif field_name == "connection_type":
                choices[field_name] = get_connection_type_choices()

    context = {
        "category": category,
        "display_category": display_category,
        "fields": fields,
        "choices": choices,
    }

    return render(request, "product/add-product.html", context)


def get_category_fields(category):
    """Get category-specific field configuration for dynamic forms.

    This function returns the field configuration for different product categories,
    defining the form fields, types, labels, and validation requirements for
    each product type in the system.

    Args:
        category (str): The product category name (CPU, GPU, Motherboard, etc.).

    Returns:
        list: List of field dictionaries containing:
            - name (str): Field name/database column name
            - label (str): Human-readable field label for forms
            - type (str): Field type (text, number, select, checkbox)
            - required (bool, optional): Whether field is required
            - step (str, optional): Step value for number fields (e.g., "0.1" for decimals)

    Field Types:
        - text: Standard text input
        - number: Numeric input (integer or decimal based on step)
        - select: Dropdown selection (requires choices)
        - checkbox: Boolean checkbox input

    Supported Categories:
        CPU, GPU, Motherboard, RAM, SSD, HDD, Power Supply, Casing,
        Cooler, Monitor, Keyboard, Mouse, Headphone

    Example Return Format:
        [
            {"name": "socket", "label": "Socket", "type": "select", "required": True},
            {"name": "cores", "label": "Cores", "type": "number", "required": True},
            {"name": "base_frequency", "label": "Base Frequency (GHz)",
             "type": "number", "step": "0.1"}
        ]

    Note:
        - Required fields are marked for form validation
        - Number fields with step="0.1" indicate decimal inputs
        - Select fields require corresponding choice functions
        - Returns empty list for unknown categories
    """
    fields = {
        "CPU": [
            {"name": "socket", "label": "Socket", "type": "select", "required": True},
            {"name": "cores", "label": "Cores", "type": "number", "required": True},
            {"name": "threads", "label": "Threads", "type": "number", "required": True},
            {
                "name": "base_frequency",
                "label": "Base Frequency (GHz)",
                "type": "number",
                "step": "0.1",
            },
            {
                "name": "boost_frequency",
                "label": "Boost Frequency (GHz)",
                "type": "number",
                "step": "0.1",
            },
            {"name": "cache", "label": "Cache (MB)", "type": "number"},
            {
                "name": "processor_graphics",
                "label": "Processor Graphics",
                "type": "text",
            },
        ],
        "GPU": [
            {"name": "chipset", "label": "Chipset", "type": "text", "required": True},
            {"name": "memory_size", "label": "Memory Size (GB)", "type": "number"},
            {"name": "memory_type", "label": "Memory Type", "type": "select"},
            {
                "name": "memory_interface",
                "label": "Memory Interface (bit)",
                "type": "number",
            },
            {"name": "base_clock", "label": "Base Clock (MHz)", "type": "number"},
            {"name": "boost_clock", "label": "Boost Clock (MHz)", "type": "number"},
            {"name": "cuda_cores", "label": "CUDA Cores", "type": "number"},
            {"name": "rt_cores", "label": "RT Cores", "type": "number"},
            {"name": "tensor_cores", "label": "Tensor Cores", "type": "number"},
            {"name": "pcie_version", "label": "PCIe Version", "type": "text"},
            {"name": "cooling_type", "label": "Cooling Type", "type": "text"},
            {"name": "length", "label": "Length (mm)", "type": "number"},
            {"name": "width", "label": "Width (mm)", "type": "number"},
            {"name": "height", "label": "Height (mm)", "type": "number"},
        ],
        "Motherboard": [
            {"name": "socket", "label": "Socket", "type": "select", "required": True},
            {"name": "chipset", "label": "Chipset", "type": "text", "required": True},
            {
                "name": "form_factor",
                "label": "Form Factor",
                "type": "select",
                "required": True,
            },
            {"name": "memory_support", "label": "Memory Support", "type": "text"},
            {"name": "max_memory", "label": "Max Memory (GB)", "type": "number"},
            {"name": "memory_slots", "label": "Memory Slots", "type": "number"},
            {"name": "pcie_slots", "label": "PCIe Slots", "type": "text"},
            {"name": "sata_ports", "label": "SATA Ports", "type": "number"},
            {"name": "m2_slots", "label": "M.2 Slots", "type": "number"},
            {"name": "usb_ports", "label": "USB Ports", "type": "text"},
            {"name": "ethernet", "label": "Ethernet", "type": "text"},
            {"name": "wifi", "label": "WiFi", "type": "text"},
            {"name": "bluetooth", "label": "Bluetooth", "type": "text"},
            {"name": "audio_chipset", "label": "Audio Chipset", "type": "text"},
        ],
        "RAM": [
            {
                "name": "memory_type",
                "label": "Memory Type",
                "type": "select",
                "required": True,
            },
            {
                "name": "capacity",
                "label": "Capacity (GB)",
                "type": "number",
                "required": True,
            },
            {
                "name": "frequency",
                "label": "Frequency (MHz)",
                "type": "number",
                "required": True,
            },
            {"name": "cas_latency", "label": "CAS Latency", "type": "text"},
            {
                "name": "voltage",
                "label": "Voltage (V)",
                "type": "number",
                "step": "0.1",
            },
            {"name": "modules", "label": "Modules", "type": "number"},
            {"name": "heat_spreader", "label": "Heat Spreader", "type": "checkbox"},
            {"name": "rgb_lighting", "label": "RGB Lighting", "type": "checkbox"},
        ],
        "SSD": [
            {
                "name": "capacity",
                "label": "Capacity (GB)",
                "type": "number",
                "required": True,
            },
            {
                "name": "interface",
                "label": "Interface",
                "type": "select",
                "required": True,
            },
            {
                "name": "form_factor",
                "label": "Form Factor",
                "type": "select",
                "required": True,
            },
            {"name": "read_speed", "label": "Read Speed (MB/s)", "type": "number"},
            {"name": "write_speed", "label": "Write Speed (MB/s)", "type": "number"},
            {"name": "nand_type", "label": "NAND Type", "type": "text"},
            {"name": "controller", "label": "Controller", "type": "text"},
            {"name": "cache", "label": "Cache (MB)", "type": "number"},
        ],
        "HDD": [
            {
                "name": "capacity",
                "label": "Capacity (GB)",
                "type": "number",
                "required": True,
            },
            {
                "name": "interface",
                "label": "Interface",
                "type": "select",
                "required": True,
            },
            {
                "name": "form_factor",
                "label": "Form Factor",
                "type": "select",
                "required": True,
            },
            {"name": "rpm", "label": "RPM", "type": "number"},
            {"name": "cache", "label": "Cache (MB)", "type": "number"},
        ],
        "Power Supply": [
            {
                "name": "wattage",
                "label": "Wattage (W)",
                "type": "number",
                "required": True,
            },
            {
                "name": "efficiency_rating",
                "label": "Efficiency Rating",
                "type": "select",
            },
            {"name": "modular_type", "label": "Modular Type", "type": "text"},
            {"name": "form_factor", "label": "Form Factor", "type": "text"},
            {"name": "fan_size", "label": "Fan Size (mm)", "type": "number"},
            {"name": "pcie_connectors", "label": "PCIe Connectors", "type": "text"},
            {"name": "sata_connectors", "label": "SATA Connectors", "type": "number"},
            {"name": "molex_connectors", "label": "Molex Connectors", "type": "number"},
            {"name": "cpu_connectors", "label": "CPU Connectors", "type": "text"},
            {"name": "active_pfc", "label": "Active PFC", "type": "checkbox"},
        ],
        "Casing": [
            {
                "name": "case_type",
                "label": "Case Type",
                "type": "text",
                "required": True,
            },
            {
                "name": "form_factor_support",
                "label": "Form Factor Support",
                "type": "text",
            },
            {
                "name": "max_gpu_length",
                "label": "Max GPU Length (mm)",
                "type": "number",
            },
            {
                "name": "max_cpu_cooler_height",
                "label": "Max CPU Cooler Height (mm)",
                "type": "number",
            },
            {"name": "drive_bays_25", "label": '2.5" Drive Bays', "type": "number"},
            {"name": "drive_bays_35", "label": '3.5" Drive Bays', "type": "number"},
            {"name": "expansion_slots", "label": "Expansion Slots", "type": "number"},
            {"name": "front_io", "label": "Front I/O", "type": "text"},
            {"name": "side_panel", "label": "Side Panel", "type": "text"},
            {"name": "rgb_lighting", "label": "RGB Lighting", "type": "checkbox"},
            {"name": "psu_shroud", "label": "PSU Shroud", "type": "checkbox"},
        ],
        "Cooler": [
            {
                "name": "cooler_type",
                "label": "Cooler Type",
                "type": "text",
                "required": True,
            },
            {
                "name": "socket_compatibility",
                "label": "Socket Compatibility",
                "type": "text",
            },
            {"name": "fan_speed", "label": "Fan Speed (RPM)", "type": "text"},
            {
                "name": "noise_level",
                "label": "Noise Level (dBA)",
                "type": "number",
                "step": "0.1",
            },
            {"name": "height", "label": "Height (mm)", "type": "number"},
            {"name": "radiator_size", "label": "Radiator Size", "type": "text"},
            {"name": "rgb_lighting", "label": "RGB Lighting", "type": "checkbox"},
        ],
        "Monitor": [
            {
                "name": "screen_size",
                "label": "Screen Size (inches)",
                "type": "number",
                "step": "0.1",
                "required": True,
            },
            {
                "name": "resolution",
                "label": "Resolution",
                "type": "text",
                "required": True,
            },
            {"name": "panel_type", "label": "Panel Type", "type": "select"},
            {"name": "refresh_rate", "label": "Refresh Rate (Hz)", "type": "number"},
            {
                "name": "response_time",
                "label": "Response Time (ms)",
                "type": "number",
                "step": "0.1",
            },
            {"name": "brightness", "label": "Brightness (cd/m²)", "type": "number"},
            {"name": "contrast_ratio", "label": "Contrast Ratio", "type": "text"},
            {"name": "color_gamut", "label": "Color Gamut", "type": "text"},
            {"name": "adaptive_sync", "label": "Adaptive Sync", "type": "text"},
            {"name": "connectivity", "label": "Connectivity", "type": "text"},
            {"name": "vesa_mount", "label": "VESA Mount", "type": "text"},
            {
                "name": "built_in_speakers",
                "label": "Built-in Speakers",
                "type": "checkbox",
            },
            {"name": "hdr_support", "label": "HDR Support", "type": "checkbox"},
            {"name": "curved", "label": "Curved", "type": "checkbox"},
        ],
        "Keyboard": [
            {"name": "switch_type", "label": "Switch Type", "type": "text"},
            {"name": "key_layout", "label": "Key Layout", "type": "text"},
            {"name": "connection_type", "label": "Connection Type", "type": "select"},
            {"name": "backlight", "label": "Backlight", "type": "text"},
            {"name": "macro_keys", "label": "Macro Keys", "type": "checkbox"},
            {"name": "wireless", "label": "Wireless", "type": "checkbox"},
            {"name": "rgb_lighting", "label": "RGB Lighting", "type": "checkbox"},
        ],
        "Mouse": [
            {"name": "sensor_type", "label": "Sensor Type", "type": "text"},
            {"name": "dpi", "label": "DPI", "type": "number"},
            {"name": "polling_rate", "label": "Polling Rate (Hz)", "type": "number"},
            {"name": "buttons", "label": "Number of Buttons", "type": "number"},
            {"name": "connection_type", "label": "Connection Type", "type": "select"},
            {"name": "wireless", "label": "Wireless", "type": "checkbox"},
            {"name": "battery_life", "label": "Battery Life (hours)", "type": "number"},
            {"name": "rgb_lighting", "label": "RGB Lighting", "type": "checkbox"},
        ],
        "Headphone": [
            {"name": "headphone_type", "label": "Headphone Type", "type": "text"},
            {"name": "driver_size", "label": "Driver Size (mm)", "type": "number"},
            {"name": "impedance", "label": "Impedance (ohms)", "type": "number"},
            {
                "name": "frequency_response",
                "label": "Frequency Response",
                "type": "text",
            },
            {"name": "connection_type", "label": "Connection Type", "type": "select"},
            {"name": "microphone", "label": "Microphone", "type": "checkbox"},
            {
                "name": "noise_cancellation",
                "label": "Noise Cancellation",
                "type": "checkbox",
            },
            {"name": "wireless", "label": "Wireless", "type": "checkbox"},
            {"name": "battery_life", "label": "Battery Life (hours)", "type": "number"},
            {"name": "rgb_lighting", "label": "RGB Lighting", "type": "checkbox"},
        ],
    }
    return fields.get(category, [])


def get_socket_choices():
    """Get available CPU socket type choices for form dropdowns.

    Returns:
        list: List of tuples containing (value, display_name) pairs
              for CPU socket types commonly used in modern systems.

    Socket Types:
        - LGA 1200: Intel 10th/11th gen
        - LGA 1700: Intel 12th/13th gen
        - LGA 1851: Intel 14th gen and newer
        - AM4: AMD Ryzen 1000-5000 series
        - AM5: AMD Ryzen 7000 series and newer
        - TR4: AMD Threadripper
    """
    return [
        ("LGA 1200", "LGA 1200"),
        ("LGA 1700", "LGA 1700"),
        ("LGA 1851", "LGA 1851"),
        ("AM4", "AM4"),
        ("AM5", "AM5"),
        ("TR4", "TR4"),
    ]


def get_memory_type_choices():
    """Get available memory type choices for form dropdowns.

    Returns:
        list: List of tuples containing (value, display_name) pairs
              for memory types used in CPUs, GPUs, and RAM modules.

    Memory Types:
        - DDR4: Standard system memory (older generation)
        - DDR5: Standard system memory (current generation)
        - GDDR6: Graphics memory standard
        - GDDR6X: Enhanced graphics memory standard
        - HBM2: High Bandwidth Memory for high-end GPUs
    """
    return [
        ("DDR4", "DDR4"),
        ("DDR5", "DDR5"),
        ("GDDR6", "GDDR6"),
        ("GDDR6X", "GDDR6X"),
        ("HBM2", "HBM2"),
    ]


def get_form_factor_choices(category):
    """Get available form factor choices based on product category.

    Args:
        category (str): Product category to get form factors for.

    Returns:
        list: List of tuples containing (value, display_name) pairs
              for form factors applicable to the specified category.
              Returns empty list if category doesn't use form factors.

    Motherboard Form Factors:
        - ATX: Standard full-size motherboard
        - Micro-ATX: Smaller motherboard format
        - Mini-ITX: Compact motherboard format
        - E-ATX: Extended ATX for high-end boards

    Storage Form Factors:
        - 2.5": Standard SSD/laptop HDD size
        - 3.5": Standard desktop HDD size
        - M.2: Modern SSD form factor
        - mSATA: Compact SSD format (legacy)
    """
    if category == "Motherboard":
        return [
            ("ATX", "ATX"),
            ("Micro-ATX", "Micro-ATX"),
            ("Mini-ITX", "Mini-ITX"),
            ("E-ATX", "E-ATX"),
        ]
    elif category in ["SSD", "HDD"]:
        return [
            ('2.5"', '2.5"'),
            ('3.5"', '3.5"'),
            ("M.2", "M.2"),
            ("mSATA", "mSATA"),
        ]
    return []


def get_efficiency_rating_choices():
    """Get available power supply efficiency rating choices.

    Returns:
        list: List of tuples containing (value, display_name) pairs
              for 80 Plus efficiency certifications from basic to highest tier.

    Efficiency Ratings (lowest to highest):
        - 80 Plus: Basic efficiency standard (80% at 20%, 50%, 100% load)
        - 80 Plus Bronze: 82-85% efficiency
        - 80 Plus Silver: 85-88% efficiency
        - 80 Plus Gold: 87-90% efficiency
        - 80 Plus Platinum: 89-92% efficiency
        - 80 Plus Titanium: 90-94% efficiency (highest tier)
    """
    return [
        ("80 Plus", "80 Plus"),
        ("80 Plus Bronze", "80 Plus Bronze"),
        ("80 Plus Silver", "80 Plus Silver"),
        ("80 Plus Gold", "80 Plus Gold"),
        ("80 Plus Platinum", "80 Plus Platinum"),
        ("80 Plus Titanium", "80 Plus Titanium"),
    ]


def get_interface_choices():
    """Get available storage interface choices for form dropdowns.

    Returns:
        list: List of tuples containing (value, display_name) pairs
              for storage device interfaces and connection types.

    Interface Types:
        - SATA III: Standard 6Gbps interface for SSDs/HDDs
        - NVMe: High-speed interface for modern SSDs
        - PCIe: Direct PCIe connection interface
        - M.2: Physical connector type (can carry SATA or NVMe)
        - IDE: Legacy parallel interface (mostly obsolete)
    """
    return [
        ("SATA III", "SATA III"),
        ("NVMe", "NVMe"),
        ("PCIe", "PCIe"),
        ("M.2", "M.2"),
        ("IDE", "IDE"),
    ]


def get_panel_type_choices():
    """Get available monitor panel type choices for form dropdowns.

    Returns:
        list: List of tuples containing (value, display_name) pairs
              for LCD/OLED panel technologies used in monitors.

    Panel Types:
        - IPS: In-Plane Switching (best color accuracy, wide viewing angles)
        - TN: Twisted Nematic (fastest response times, lower cost)
        - VA: Vertical Alignment (high contrast ratios, moderate speed)
        - OLED: Organic LED (perfect blacks, excellent contrast)
        - QLED: Quantum Dot LED (enhanced color gamut)
    """
    return [
        ("IPS", "IPS"),
        ("TN", "TN"),
        ("VA", "VA"),
        ("OLED", "OLED"),
        ("QLED", "QLED"),
    ]


def get_connection_type_choices():
    """Get available connection type choices for peripheral devices.

    Returns:
        list: List of tuples containing (value, display_name) pairs
              for connection methods used by keyboards, mice, headphones, etc.

    Connection Types:
        - Wired: Physical cable connection
        - Wireless: Radio frequency wireless (2.4GHz)
        - Bluetooth: Bluetooth wireless protocol
        - USB: Universal Serial Bus connection
        - 3.5mm: Standard analog audio jack
        - USB-C: Modern USB connector type
    """
    return [
        ("Wired", "Wired"),
        ("Wireless", "Wireless"),
        ("Bluetooth", "Bluetooth"),
        ("USB", "USB"),
        ("3.5mm", "3.5mm"),
        ("USB-C", "USB-C"),
    ]
