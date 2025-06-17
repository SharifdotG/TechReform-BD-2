"""
Django settings for TechReform e-commerce platform.

TechReform is a comprehensive e-commerce platform specializing in technology
products including computers, components, and accessories. This settings module
configures the Django application for both development and production environments.

Project Architecture:
    The platform consists of multiple Django apps providing specialized functionality:
    - ProductsApp: Product catalog, categories, inventory management
    - AuthApp: User authentication, role-based access, customer support
    - CartApp: Shopping cart, checkout, order processing
    - WishlistApp: Product wishlists and favorites
    - CompareApp: Product comparison functionality
    - PCBuilderApp: Custom PC configuration builder
    - BlogApp: Content management and blog functionality

Key Features:
    - Role-based user authentication (Customer, Staff, Content Manager, Blogger, Admin)
    - Comprehensive product catalog with advanced filtering
    - Shopping cart and secure checkout process
    - Customer support ticket system
    - Product comparison and wishlist functionality
    - PC builder tool for custom configurations
    - Rich text blog content with CKEditor
    - Responsive design with Tailwind CSS

Development Tools:
    - Django 5.1.3 framework
    - SQLite database for development
    - Tailwind CSS for styling
    - CKEditor for rich text content
    - Browser auto-reload for development
    - Comprehensive media file handling

Security Considerations:
    - CSRF protection enabled
    - Secure session management
    - Password validation
    - File upload security
    - Role-based access controls

For deployment configuration and production settings, refer to:
https://docs.djangoproject.com/en/5.1/howto/deployment/

For detailed Django settings reference, see:
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
import platform
from pathlib import Path
import dj_database_url

# =============================================================================
# PATH CONFIGURATION
# =============================================================================

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# This is the root directory of the Django project, used as a reference
# for all relative path configurations throughout the settings.
BASE_DIR = Path(__file__).resolve().parent.parent


# =============================================================================
# SECURITY CONFIGURATION
# =============================================================================
# SECURITY WARNING: These settings are configured for development only.
# For production deployment, ensure proper security measures are implemented.

# SECURITY WARNING: keep the secret key used in production secret!
# This key is used for cryptographic signing and should be kept confidential.
# In production, load this from environment variables or secure storage.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-^=(31@%01)s)t!0n^_*jd+)f!oflhxd@ob-j6@i7wdi*fsf44p')

# SECURITY WARNING: don't run with debug turned on in production!
# Debug mode provides detailed error pages and should never be enabled in production.
# Set to False in production for security and performance.
DEBUG = 'RENDER' not in os.environ

# Allowed hostnames that this Django site can serve.
# In production, specify the actual domain names and IP addresses.
# Example: ['techreform.com', 'www.techreform.com', '192.168.1.100']
ALLOWED_HOSTS = []

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# =============================================================================
# APPLICATION CONFIGURATION
# =============================================================================
# Django apps that are activated for this project, including both built-in
# Django apps and custom applications specific to TechReform platform.

INSTALLED_APPS = [
    # Django Core Applications
    # Essential Django functionality for admin, authentication, and basic features
    "django.contrib.admin",  # Admin interface for content management
    "django.contrib.auth",  # User authentication and permissions
    "django.contrib.contenttypes",  # Content type framework
    "django.contrib.sessions",  # Session framework for user state
    "django.contrib.messages",  # Messaging framework for user feedback
    "django.contrib.staticfiles",  # Static file serving and management
    "django.contrib.humanize",  # Template filters for human-readable data
    # TechReform Core Applications
    # Custom business logic applications specific to the e-commerce platform
    "ProductsApp",  # Product catalog, categories, inventory, and search
    "AuthApp",  # Extended authentication, user roles, and customer support
    "CartApp",  # Shopping cart, checkout process, and order management
    "WishlistApp",  # Product wishlist and favorites functionality
    "CompareApp",  # Product comparison tools and features
    "PCBuilderApp",  # Custom PC configuration and compatibility checking
    "BlogApp",  # Content management system and blog functionality
    # Third-Party Applications
    # External packages that extend Django functionality
    "tailwind",  # Tailwind CSS integration for styling
    "theme",  # Custom Tailwind theme configuration
    "django_browser_reload",  # Auto-reload browser during development
    "ckeditor",  # Rich text editor for content creation
    "ckeditor_uploader",  # File upload functionality for CKEditor
]

# =============================================================================
# TAILWIND CSS CONFIGURATION
# =============================================================================
# Configuration for Tailwind CSS integration and custom theme

# Specifies which app contains the Tailwind configuration
TAILWIND_APP_NAME = "theme"

# Internal IP addresses that can access development features
# Used for debug toolbar and browser reload functionality
INTERNAL_IPS = [
    "127.0.0.1",  # Localhost for development
]

# Path to NPM binary for Tailwind CSS compilation
# Automatically detects the correct path based on the operating system
if platform.system() == "Windows":
    NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"
else:
    # Linux/macOS - npm is typically in PATH
    NPM_BIN_PATH = "npm"


# =============================================================================
# MIDDLEWARE CONFIGURATION
# =============================================================================
# Middleware classes that process requests and responses in order

MIDDLEWARE = [
    # Security middleware - must be first for proper HTTPS handling
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise middleware for serving static files - must be after SecurityMiddleware
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # Session middleware - manages user sessions and authentication state
    "django.contrib.sessions.middleware.SessionMiddleware",
    # Common middleware - handles URL normalization and other common tasks
    "django.middleware.common.CommonMiddleware",
    # CSRF protection - prevents cross-site request forgery attacks
    "django.middleware.csrf.CsrfViewMiddleware",
    # Authentication middleware - associates users with requests
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # Messages middleware - handles temporary messages between requests
    "django.contrib.messages.middleware.MessageMiddleware",
    # Clickjacking protection - prevents pages from being embedded in frames
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Development tool - auto-reloads browser when files change (development only)
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

# =============================================================================
# URL CONFIGURATION
# =============================================================================

# Root URL configuration module
ROOT_URLCONF = "TechReform.urls"


# =============================================================================
# TEMPLATE CONFIGURATION
# =============================================================================
# Template engine configuration with context processors for global data

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # Global template directory
        "APP_DIRS": True,  # Enable app-level template directories
        "OPTIONS": {
            "context_processors": [
                # Django built-in context processors
                "django.template.context_processors.debug",  # Debug information
                "django.template.context_processors.request",  # Request object access
                "django.contrib.auth.context_processors.auth",  # User authentication data
                "django.contrib.messages.context_processors.messages",  # Message framework
                # TechReform custom context processors for global template data
                "CartApp.context_processors.cart.cart_processor",  # Shopping cart data
                "CompareApp.context_processors.compare.compare_processor",  # Product comparison data
                "WishlistApp.context_processors.wishlist.wishlist_processor",  # Wishlist data
            ],
        },
    },
]

# =============================================================================
# WSGI CONFIGURATION
# =============================================================================

# WSGI application object for deployment
WSGI_APPLICATION = "TechReform.wsgi.application"


# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================
# Database configuration - PostgreSQL for production, SQLite for development

DATABASES = {
    'default': dj_database_url.config(
        # Replace this value with your local database's connection string.
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        conn_max_age=600
    )
}


# =============================================================================
# PASSWORD VALIDATION CONFIGURATION
# =============================================================================
# Password validation rules to ensure secure user passwords

AUTH_PASSWORD_VALIDATORS = [
    {
        # Prevents passwords too similar to user information
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        # Enforces minimum password length (default: 8 characters)
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        # Prevents commonly used passwords
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        # Prevents purely numeric passwords
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# =============================================================================
# INTERNATIONALIZATION CONFIGURATION
# =============================================================================
# Localization and timezone settings for the application

# Language code for the default language
LANGUAGE_CODE = "en-us"

# Default timezone - consider changing to your local timezone
# Example: "America/New_York", "Europe/London", "Asia/Tokyo"
TIME_ZONE = "UTC"

# Enable Django's internationalization system
USE_I18N = True

# Enable timezone-aware datetime handling
USE_TZ = True


# =============================================================================
# STATIC FILES AND MEDIA CONFIGURATION
# =============================================================================
# Configuration for serving static assets and user-uploaded media files

# URL prefix for static files (CSS, JavaScript, images)
STATIC_URL = "static/"

# Directories where Django will look for static files during development
STATICFILES_DIRS = [BASE_DIR / "static"]

# Directory where all static files will be collected for production
# Run 'python manage.py collectstatic' before deploying
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

if not DEBUG:
    # Enable the WhiteNoise storage backend, which compresses static files to reduce disk use
    # and renames the files with unique names for each version to support long-term caching
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# URL prefix for user-uploaded media files
MEDIA_URL = "media/"

# Directory where user-uploaded files are stored
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# =============================================================================
# DATABASE MODEL CONFIGURATION
# =============================================================================
# Default primary key field type for auto-generated primary keys
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =============================================================================
# CKEDITOR CONFIGURATION
# =============================================================================
# Rich text editor configuration for blog content and descriptions

# Directory for CKEditor file uploads (relative to MEDIA_ROOT)
CKEDITOR_UPLOAD_PATH = "uploads/"

# Image processing backend for CKEditor
CKEDITOR_IMAGE_BACKEND = "pillow"

# jQuery library URL for CKEditor functionality
CKEDITOR_JQUERY_URL = "//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"

# Custom CKEditor toolbar configuration
# Provides a comprehensive set of editing tools for content creation
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "Custom",
        "toolbar_Custom": [
            # Text formatting tools
            ["Bold", "Italic", "Underline"],
            # List and alignment tools
            [
                "NumberedList",  # Ordered lists
                "BulletedList",  # Unordered lists
                "-",  # Separator
                "Outdent",  # Decrease indent
                "Indent",  # Increase indent
                "-",  # Separator
                "JustifyLeft",  # Left align
                "JustifyCenter",  # Center align
                "JustifyRight",  # Right align
                "JustifyBlock",  # Justify
            ],
            # Link management
            ["Link", "Unlink"],
            # Content tools
            ["RemoveFormat", "Source"],  # Remove formatting and source view
            # Media and layout
            ["Image", "Table", "HorizontalRule"],
            # Advanced formatting
            ["Styles", "Format", "Font", "FontSize", "TextColor", "BGColor"],
        ],
        # Editor dimensions
        "height": 400,  # Editor height in pixels
        "width": "100%",  # Editor width (responsive)
    },
}
