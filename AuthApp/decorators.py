"""
Authentication decorators for role-based access control.

This module provides a collection of decorators for Django views that implement
role-based access control. The decorators check user authentication status and
user roles before allowing access to protected views.

Available decorators:
    - role_required: Generic decorator that accepts role(s) as parameter
    - admin_required: Requires admin role
    - staff_required: Requires admin or staff role
    - content_manager_required: Requires admin or content_manager role
    - blogger_required: Requires admin or blogger role
    - user_required: Allows any authenticated user with a valid role
"""

from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps
from .models import UserProfile


def role_required(roles):
    """
    Decorator for views that checks whether a user has a specific role.

    This decorator verifies that the user is authenticated and has one of the
    specified roles. If the user doesn't have the required role, they are
    redirected with an error message. Superusers bypass role checks.

    Args:
        roles (str or list): A single role string or list of allowed roles.
                           Valid roles: 'admin', 'staff', 'content_manager',
                           'blogger', 'user'

    Returns:
        function: The decorated view function with role checking applied.

    Redirects:
        - To login page if user is not authenticated
        - To index page with error message if user lacks required role

    Example:
        @role_required('admin')
        def admin_view(request):
            return render(request, 'admin_page.html')

        @role_required(['admin', 'staff'])
        def staff_view(request):
            return render(request, 'staff_page.html')
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")

            if not hasattr(request.user, "profile"):
                UserProfile.objects.create(user=request.user)

            # Check if the user has one of the required roles
            if isinstance(roles, str):
                role_check = request.user.profile.role == roles
            else:
                role_check = request.user.profile.role in roles

            if role_check or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(
                    request, "You don't have permission to access this page."
                )
                return redirect("index")

        return _wrapped_view

    return decorator


def admin_required(view_func):
    """
    Decorator for views that require admin role.

    This is a convenience decorator that restricts access to admin users only.
    Superusers are automatically granted access regardless of their profile role.

    Args:
        view_func (function): The view function to be decorated.

    Returns:
        function: The decorated view function with admin role checking.

    Example:
        @admin_required
        def admin_dashboard(request):
            return render(request, 'admin/dashboard.html')
    """
    return role_required("admin")(view_func)


def staff_required(view_func):
    """
    Decorator for views that require staff or admin role.

    This decorator allows access to users with either 'staff' or 'admin' roles.
    Useful for views that need elevated permissions but not full admin access.

    Args:
        view_func (function): The view function to be decorated.

    Returns:
        function: The decorated view function with staff/admin role checking.

    Example:
        @staff_required
        def staff_panel(request):
            return render(request, 'staff/panel.html')
    """
    return role_required(["admin", "staff"])(view_func)


def content_manager_required(view_func):
    """
    Decorator for views that require content manager or admin role.

    This decorator is designed for content management functionality, allowing
    access to users with 'content_manager' or 'admin' roles.

    Args:
        view_func (function): The view function to be decorated.

    Returns:
        function: The decorated view function with content manager/admin role checking.

    Example:
        @content_manager_required
        def manage_content(request):
            return render(request, 'content/manage.html')
    """
    return role_required(["admin", "content_manager"])(view_func)


def blogger_required(view_func):
    """
    Decorator for views that require blogger or admin role.

    This decorator is specifically for blog-related functionality, allowing
    access to users with 'blogger' or 'admin' roles.

    Args:
        view_func (function): The view function to be decorated.

    Returns:
        function: The decorated view function with blogger/admin role checking.

    Example:
        @blogger_required
        def create_blog_post(request):
            return render(request, 'blog/create.html')
    """
    return role_required(["admin", "blogger"])(view_func)


def user_required(view_func):
    """
    Decorator for views that require any authenticated user with a valid role.

    This decorator allows access to any authenticated user with a recognized role
    in the system. It's the most permissive decorator and is used for general
    user-accessible features.

    Args:
        view_func (function): The view function to be decorated.

    Returns:
        function: The decorated view function with basic user role checking.

    Example:
        @user_required
        def user_profile(request):
            return render(request, 'user/profile.html')
    """
    return role_required(["admin", "staff", "content_manager", "blogger", "user"])(
        view_func
    )
