from django.db import migrations


def forward_cart_data(apps, schema_editor):
    """
    This migration was designed to migrate data from TechReformApp to CartApp,
    but since TechReformApp doesn't exist in the current project structure,
    this migration is now a no-op (no operation).

    The project already uses the modular app structure with CartApp,
    so no data migration is needed.
    """
    # No operation - no data to migrate since TechReformApp doesn't exist
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("CartApp", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(forward_cart_data),
    ]
