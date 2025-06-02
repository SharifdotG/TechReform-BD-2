"""
Wishlist context processor module.

This module provides context processors that make wishlist-related data
available to all Django templates across the application.
"""

from ..models import WishList, WishlistItem


def wishlist_processor(request):
    """
    Context processor to make wishlist data available to all templates.

    This function is designed to be used as a Django context processor,
    automatically providing wishlist information to every template rendered
    in the application. It handles both authenticated and anonymous users
    by creating or retrieving wishlists based on user authentication status
    or session information.

    Args:
        request (HttpRequest): The Django HTTP request object containing
            user authentication information and session data.

    Returns:
        dict: A dictionary containing wishlist context variables:
            - wishlist_count (int): The total number of items in the user's wishlist
            - wishlist_items (QuerySet): A QuerySet of WishlistItem objects
              belonging to the current user's wishlist

    Note:
        - For authenticated users, wishlists are associated with the user account
        - For anonymous users, wishlists are associated with the session ID
        - A new wishlist is automatically created if one doesn't exist
        - Session keys are created automatically for anonymous users if needed

    Example:
        In templates, you can access wishlist data like:
        {{ wishlist_count }} - displays the number of wishlist items
        {% for item in wishlist_items %} - iterates through wishlist items
    """
    wishlist_count = 0
    wishlist_items = []

    # Try to get the wishlist for the current user/session
    if request.user.is_authenticated:
        # For authenticated users
        wishlist, created = WishList.objects.get_or_create(user=request.user)
        wishlist_items = WishlistItem.objects.filter(wishlist=wishlist)
    else:
        # For anonymous users
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        wishlist, created = WishList.objects.get_or_create(session_id=session_key)
        wishlist_items = WishlistItem.objects.filter(wishlist=wishlist)

    wishlist_count = wishlist_items.count()

    # Return the context variables
    return {"wishlist_count": wishlist_count, "wishlist_items": wishlist_items}
