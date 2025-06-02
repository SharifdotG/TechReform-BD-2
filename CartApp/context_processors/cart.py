"""Django context processor for cart functionality.

This module provides a context processor that makes cart data globally available
across all templates in the TechReform application. It handles both authenticated
user carts and anonymous session-based carts, ensuring seamless shopping cart
functionality regardless of user authentication status.

The context processor automatically creates and manages cart sessions for
anonymous users and links carts to user accounts for authenticated users.
This enables persistent cart functionality and smooth user experience transitions
between anonymous browsing and logged-in shopping.

Key Features:
- Global cart context availability in all templates
- Automatic cart creation for new users/sessions
- Session-based cart tracking for anonymous users
- User-based cart persistence for authenticated users
- Error handling with graceful fallbacks
"""

import uuid
from ..models import Cart


def cart_processor(request):
    """Make cart data globally available in all template contexts.

    This context processor ensures that cart information is available in every
    template without requiring individual views to pass cart data. It handles
    both authenticated and anonymous users with different cart tracking strategies.

    For authenticated users:
        - Links cart to user account for persistence across sessions
        - Automatically creates a cart if none exists for the user

    For anonymous users:
        - Uses session-based tracking with UUID session identifiers
        - Creates new session ID if none exists
        - Maintains cart state across page loads during session

    Args:
        request (HttpRequest): The Django request object containing user and session data

    Returns:
        dict: Context dictionary containing cart data with keys:
            - cart_count (int): Total number of items in the cart
            - cart_total (Decimal): Total monetary value of cart contents
            - cart (Cart|None): The complete Cart model instance for template access

    Error Handling:
        Returns safe default values (0 counts, None cart) if any exceptions occur
        during cart retrieval or creation to prevent template rendering failures.

    Session Management:
        Automatically manages session modification flags to ensure session
        persistence when creating new session IDs for anonymous users.

    Note:
        This context processor must be registered in Django settings.py under
        TEMPLATES['OPTIONS']['context_processors'] to function globally.
    """
    try:
        if request.user.is_authenticated:
            # If user is logged in, get or create their cart
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            # If anonymous user, use session ID to track cart
            session_id = request.session.get("cart_session_id")
            if not session_id:
                # Create a new session ID if one doesn't exist
                session_id = str(uuid.uuid4())
                request.session["cart_session_id"] = session_id
                # Make sure session is saved
                request.session.modified = True

            # Get or create cart with the session ID
            cart, created = Cart.objects.get_or_create(session_id=session_id)

        return {
            "cart_count": cart.get_cart_items_count,
            "cart_total": cart.get_cart_total,
            "cart": cart,  # Include the entire cart object for more flexibility in templates
        }
    except Exception:
        # Return empty dict if any errors occur
        return {"cart_count": 0, "cart_total": 0, "cart": None}
