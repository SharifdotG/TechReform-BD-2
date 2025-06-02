"""URL Configuration for ProductsApp.

This module defines the URL patterns for the ProductsApp, which handles
product-related functionality including product listings, details, category
filtering, and administrative product management operations.

URL Patterns:
    - Public product views (index, about, FAQ, product listings)
    - Product detail and category views
    - Administrative product management (add, update, delete, toggle status)
    - Newsletter subscription functionality

All product-related URLs are mapped to their corresponding view functions
in the ProductsApp.views module.
"""

from django.urls import path
from . import views

# URL patterns for ProductsApp
urlpatterns = [
    # Public information pages
    path("", views.index, name="index"),
    path("about-us/", views.about_us, name="about-us"),
    path("faq/", views.faq, name="faq"),
    # Product browsing URLs
    path("product-list/", views.product_list, name="product-list"),
    path("product/<uuid:product_id>/", views.product_detail, name="product-detail"),
    path(
        "category/<str:category_name>/",
        views.category_products,
        name="category_products",
    ),
    path("featured/", views.featured_products, name="featured_products"),
    path("new-arrivals/", views.new_arrivals, name="new_arrivals"),
    path("deals/", views.deals_products, name="deals_products"),
    # Administrative product management URLs
    path("manage-products/", views.product_management, name="product_management"),
    path("add-product/<str:category>/", views.add_product, name="add_product"),
    path(
        "update-product/<uuid:product_id>/<str:category>/",
        views.update_product,
        name="update_product",
    ),
    path(
        "toggle-product-status/<uuid:product_id>/<str:product_type>/",
        views.toggle_product_status,
        name="toggle_product_status",
    ),
    path(
        "delete-product/<uuid:product_id>/<str:product_type>/",
        views.delete_product,
        name="delete_product",
    ),
    # Miscellaneous functionality
    path(
        "newsletter/subscribe/", views.newsletter_subscribe, name="newsletter_subscribe"
    ),
]
