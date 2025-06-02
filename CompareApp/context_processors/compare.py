"""
Django context processor for product comparison functionality.

This module provides a context processor that makes product comparison data
globally available across all templates in the TechReform application. It
handles both authenticated user comparison lists and anonymous session-based
comparison lists, enabling seamless product comparison functionality.

The context processor automatically creates and manages comparison sessions
for anonymous users and links comparison lists to user accounts for authenticated
users. This ensures persistent comparison functionality and smooth transitions
between anonymous browsing and logged-in shopping experiences.

Key Features:
    - Global comparison context availability in all templates
    - Automatic comparison list creation for new users/sessions
    - Session-based comparison tracking for anonymous users
    - User-based comparison persistence for authenticated users
    - Real-time comparison count for UI elements
    - Support for multiple product categories in comparisons

The processor provides:
    - compare_count: Number of items in comparison list
    - compare_items: QuerySet of items in the comparison list
    - compare_list: The comparison list object itself

This enables templates to display comparison indicators, counts, and
quick access to comparison functionality without requiring explicit
view-level context management.
"""

from ..models import CompareList, CompareItem


def compare_processor(request):
    """
    Context processor to make compare data available to all templates
    """
    compare_count = 0
    compare_items = []

    # Try to get the compare list for the current user/session
    if request.user.is_authenticated:
        # For authenticated users
        compare_list, created = CompareList.objects.get_or_create(user=request.user)
        compare_items = CompareItem.objects.filter(compare_list=compare_list)
    else:
        # For anonymous users
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        compare_list, created = CompareList.objects.get_or_create(
            session_id=session_key
        )
        compare_items = CompareItem.objects.filter(compare_list=compare_list)

    compare_count = compare_items.count()

    # Return the context variables
    return {"compare_count": compare_count, "compare_items": compare_items}
