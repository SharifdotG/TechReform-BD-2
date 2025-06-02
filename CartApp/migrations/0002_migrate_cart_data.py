from django.db import migrations


def forward_cart_data(apps, schema_editor):
    """
    Migrates cart data from TechReformApp to CartApp
    """
    # Get old and new models
    OldCart = apps.get_model("TechReformApp", "Cart")
    NewCart = apps.get_model("CartApp", "Cart")
    OldCartItem = apps.get_model("TechReformApp", "CartItem")
    NewCartItem = apps.get_model("CartApp", "CartItem")
    OldOrder = apps.get_model("TechReformApp", "Order")
    NewOrder = apps.get_model("CartApp", "Order")
    OldOrderItem = apps.get_model("TechReformApp", "OrderItem")
    NewOrderItem = apps.get_model("CartApp", "OrderItem")
    OldShippingAddress = apps.get_model("TechReformApp", "ShippingAddress")
    NewShippingAddress = apps.get_model("CartApp", "ShippingAddress")

    # Copy cart data - handle the case where a user might have multiple carts
    for old_cart in OldCart.objects.all():
        # Check if a cart already exists for this user
        existing_cart = None
        if old_cart.user:
            try:
                existing_cart = NewCart.objects.get(user=old_cart.user)
            except NewCart.DoesNotExist:
                pass

        if existing_cart:
            # Use the existing cart
            new_cart = existing_cart
        else:
            # Create new cart with the same ID to maintain reference
            new_cart = NewCart.objects.create(
                id=old_cart.id,
                user=old_cart.user,
                session_id=old_cart.session_id,
                created_at=old_cart.created_at,
                updated_at=old_cart.updated_at,
            )

        # Copy cart items
        for old_item in OldCartItem.objects.filter(cart=old_cart):
            NewCartItem.objects.create(
                id=old_item.id,
                cart=new_cart,
                product_id=old_item.product_id,
                product_category=old_item.product_category,
                quantity=old_item.quantity,
                price=old_item.price,
                created_at=old_item.created_at,
                updated_at=old_item.updated_at,
            )

    # Copy order data
    for old_order in OldOrder.objects.all():
        # Create new order with the same ID to maintain reference
        new_order = NewOrder.objects.create(
            id=old_order.id,
            user=old_order.user,
            order_number=old_order.order_number,
            status=old_order.status,
            payment_method=old_order.payment_method,
            payment_status=old_order.payment_status,
            tax=old_order.tax,
            shipping_cost=old_order.shipping_cost,
            total_price=old_order.total_price,
            notes=old_order.notes,
            ip_address=old_order.ip_address,
            created_at=old_order.created_at,
            updated_at=old_order.updated_at,
            payment_date=old_order.payment_date,
            shipped_date=old_order.shipped_date,
            delivered_date=old_order.delivered_date,
        )

        # Copy order items
        for old_item in OldOrderItem.objects.filter(order=old_order):
            NewOrderItem.objects.create(
                id=old_item.id,
                order=new_order,
                product_id=old_item.product_id,
                product_category=old_item.product_category,
                product_name=old_item.product_name,
                quantity=old_item.quantity,
                price=old_item.price,
                created_at=old_item.created_at,
            )

        # Copy shipping address if exists
        try:
            old_address = OldShippingAddress.objects.get(order=old_order)
            NewShippingAddress.objects.create(
                id=old_address.id,
                order=new_order,
                user=old_address.user,
                full_name=old_address.full_name,
                phone=old_address.phone,
                email=old_address.email,
                address_line1=old_address.address_line1,
                address_line2=old_address.address_line2,
                city=old_address.city,
                state=old_address.state,
                postal_code=old_address.postal_code,
                created_at=old_address.created_at,
                updated_at=old_address.updated_at,
            )
        except OldShippingAddress.DoesNotExist:
            pass


class Migration(migrations.Migration):
    dependencies = [
        ("CartApp", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(forward_cart_data),
    ]
