"""
Django views for WishlistApp.

This module contains view functions that handle all wishlist-related
operations in the TechReform e-commerce application. It provides
functionality for managing user wishlists including adding products,
removing items, clearing wishlists, and displaying wishlist contents.

The module supports both authenticated and anonymous users by using
session-based storage for guest users and user-associated storage
for registered users.

Key Features:
    - Add products to wishlist (AJAX and form support)
    - Remove individual items from wishlist
    - Clear entire wishlist
    - View wishlist with product details
    - Support for multiple product categories
    - Session-based wishlist for anonymous users
    - User-based wishlist for authenticated users
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import WishList, WishlistItem
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
    """
    Retrieve a product object by its ID and category.

    This helper function maps product categories to their corresponding
    Django model classes and retrieves the specific product instance.
    It supports all product categories available in the e-commerce system.

    Args:
        product_id (str): The unique identifier of the product.
        category (str): The category of the product (e.g., 'CPU', 'GPU', etc.).

    Returns:
        Model instance or None: The product object if found, None if the
        category is not recognized or if the product doesn't exist.

    Raises:
        Http404: If the product with the given ID doesn't exist in the
        specified category.

    Supported Categories:
        CPU, GPU, RAM, SSD, HDD, Power Supply, Casing, Cooler,
        Monitor, Motherboard, Keyboard, Mouse, Headphone
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


def get_wishlist(request):
    """
    Get or create a wishlist for the current user or session.

    This helper function handles wishlist retrieval for both authenticated
    and anonymous users. For authenticated users, wishlists are associated
    with their user account. For anonymous users, wishlists are associated
    with their session ID.

    Args:
        request (HttpRequest): The Django HTTP request object containing
            user authentication information and session data.

    Returns:
        WishList: The wishlist instance for the current user or session.
            A new wishlist is created if one doesn't exist.

    Note:
        - For anonymous users, a session key is automatically created if
          one doesn't exist.
        - Each authenticated user can have only one wishlist (OneToOne relationship).
        - Anonymous users' wishlists are identified by session ID.
    """
    if request.user.is_authenticated:
        try:
            wishlist = WishList.objects.get(user=request.user)
        except WishList.DoesNotExist:
            wishlist = WishList.objects.create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_id = request.session.session_key
        try:
            wishlist = WishList.objects.get(session_id=session_id)
        except WishList.DoesNotExist:
            wishlist = WishList.objects.create(session_id=session_id)

    return wishlist


@require_POST
def add_to_wishlist(request):
    """
    Add a product to the user's wishlist.

    This view function handles adding products to wishlists for both
    authenticated and anonymous users. It supports both AJAX requests
    (returning JSON responses) and regular form submissions. The function
    performs validation, duplicate checking, and provides appropriate
    feedback messages.

    Args:
        request (HttpRequest): The Django HTTP request object. Must be a POST
            request containing 'product_id' and 'product_category' parameters.

    Returns:
        JsonResponse: For AJAX requests, returns JSON with status, message,
            and updated wishlist count.
        HttpResponseRedirect: For regular requests, redirects to appropriate
            page with success/error messages.

    POST Parameters:
        product_id (str): The unique identifier of the product to add.
        product_category (str): The category of the product.

    Raises:
        Http404: If the specified product doesn't exist.

    Response Format (AJAX):
        {
            "status": "success|error|info",
            "message": "Human-readable message",
            "wishlist_count": integer (on success)
        }

    Note:
        - Prevents duplicate entries in the wishlist
        - Automatically associates items with user account if authenticated
        - Creates session-based entries for anonymous users
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

        # Get or create the wishlist for the current user/session
        wishlist = get_wishlist(request)

        # Check if this product is already in the wishlist
        existing_item = WishlistItem.objects.filter(
            wishlist=wishlist, product_id=product_id, category=product_category
        ).first()

        if existing_item:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse(
                    {
                        "status": "info",
                        "message": "This product is already in your wishlist",
                        "wishlist_count": wishlist.get_wishlist_items_count,
                    }
                )
            messages.info(request, "This product is already in your wishlist")
            return redirect("view_wishlist")

        # Add the item to the wishlist
        wishlist_item = WishlistItem(
            wishlist=wishlist, product_id=product_id, category=product_category
        )

        # If user is authenticated, associate the item with the user as well
        if request.user.is_authenticated:
            wishlist_item.user = request.user

        wishlist_item.save()

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse(
                {
                    "status": "success",
                    "message": "Product added to your wishlist",
                    "wishlist_count": wishlist.get_wishlist_items_count,
                }
            )

        messages.success(request, "Product added to your wishlist")
        return redirect("view_wishlist")

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
def remove_from_wishlist(request):
    """
    Remove a specific product from the user's wishlist.

    This view function handles the removal of individual wishlist items.
    It includes permission checking to ensure users can only remove items
    from their own wishlists, providing security for both authenticated
    and anonymous users.

    Args:
        request (HttpRequest): The Django HTTP request object. Must be a POST
            request containing 'item_id' parameter.

    Returns:
        HttpResponseRedirect: Redirects to the wishlist view page with
            appropriate success or error messages.

    POST Parameters:
        item_id (str): The unique identifier of the wishlist item to remove.

    Security:
        - Authenticated users can only remove items from their own wishlist
        - Anonymous users can remove items from their session-based wishlist
        - Prevents unauthorized access to other users' wishlist items

    Raises:
        Http404: If the wishlist item with the given ID doesn't exist.

    Note:
        - Provides user feedback through Django messages framework
        - Automatically redirects to wishlist view after operation
        - Validates user permissions before performing deletion
    """
    if request.method == "POST":
        item_id = request.POST.get("item_id")

        if not item_id:
            messages.error(request, "Item ID is required")
            return redirect("view_wishlist")

        # Get the wishlist item
        wishlist_item = get_object_or_404(WishlistItem, id=item_id)

        # Check if the user has permission to delete this item
        if (
            request.user.is_authenticated
            and wishlist_item.user
            and wishlist_item.user != request.user
        ):
            messages.error(request, "You do not have permission to remove this item")
            return redirect("view_wishlist")

        # Delete the item
        wishlist_item.delete()

        messages.success(request, "Product removed from your wishlist")
        return redirect("view_wishlist")

    return redirect("view_wishlist")


@require_POST
def clear_wishlist(request):
    """
    Clear all items from the user's wishlist.

    This view function removes all items from the current user's wishlist,
    effectively clearing it completely. It handles both authenticated and
    anonymous user wishlists appropriately.

    Args:
        request (HttpRequest): The Django HTTP request object. Must be a POST
            request for security purposes.

    Returns:
        HttpResponseRedirect: Redirects to the wishlist view page with
            a success message confirming the clearance.

    Security:
        - Only accepts POST requests to prevent accidental clearing
        - Handles session-based wishlists for anonymous users
        - Handles user-based wishlists for authenticated users

    Note:
        - Deletes all WishlistItem objects associated with the user's wishlist
        - The WishList object itself remains but becomes empty
        - Provides user feedback through Django messages framework
        - Safe to call even if the wishlist is already empty
    """
    if request.method == "POST":
        # Get the wishlist for the current user/session
        if request.user.is_authenticated:
            wishlist = WishList.objects.filter(user=request.user).first()
        else:
            session_key = request.session.session_key
            if not session_key:
                return redirect("view_wishlist")
            wishlist = WishList.objects.filter(session_id=session_key).first()

        if wishlist:
            # Delete all items in the wishlist
            WishlistItem.objects.filter(wishlist=wishlist).delete()

            messages.success(request, "Your wishlist has been cleared")

        return redirect("view_wishlist")

    return redirect("view_wishlist")


def view_wishlist(request):
    """
    Display the user's wishlist page with all wishlist items.

    This view function renders the wishlist page showing all products
    that the user has added to their wishlist. It retrieves the actual
    product objects from their respective models and provides them to
    the template for display.

    Args:
        request (HttpRequest): The Django HTTP request object containing
            user authentication information and session data.

    Returns:
        HttpResponse: Rendered wishlist template with product context.

    Template Context:
        products (list): A list of product objects from the wishlist.
            Each product object includes an additional 'wishlist_item_id'
            attribute for identification in removal operations.

    Template:
        wishlist/wishlist.html: The template used to render the wishlist page.

    Note:
        - Automatically creates a wishlist if one doesn't exist
        - Handles both authenticated and anonymous users
        - Filters out any wishlist items that reference non-existent products
        - Products retain their original model attributes plus wishlist_item_id
        - Session keys are created automatically for anonymous users
    """
    # Get the wishlist for the current user/session
    if request.user.is_authenticated:
        wishlist, created = WishList.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        wishlist, created = WishList.objects.get_or_create(session_id=session_key)

    # Get all items in the wishlist
    wishlist_items = WishlistItem.objects.filter(wishlist=wishlist)

    products = []

    # Process the items to get the actual product objects
    for item in wishlist_items:
        product = item.get_product()
        if product:
            # Add the wishlist item ID to the product for later reference
            product.wishlist_item_id = item.id
            products.append(product)

    context = {
        "products": products,
    }

    return render(request, "wishlist/wishlist.html", context)
