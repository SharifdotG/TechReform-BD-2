from django.db import migrations, connection
from django.db.backends.utils import CursorWrapper

def copy_data(apps, schema_editor):
    """
    Copy data from old TechReformApp tables to new ProductsApp tables.
    This migration is designed to handle the transition from SQLite to PostgreSQL.
    It will skip execution if the source tables don't exist (e.g., on fresh PostgreSQL).
    """
    cursor = connection.cursor()
    db_vendor = connection.vendor

    # Skip this migration on PostgreSQL if it's a fresh installation
    # (source tables won't exist)
    if db_vendor == 'postgresql':
        # Check if any of the source tables exist
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name LIKE 'TechReformApp_%'
        """)
        existing_source_tables = [row[0] for row in cursor.fetchall()]

        if not existing_source_tables:
            # No source tables found, skip this migration
            return

    # Define table mappings (source_table, destination_table)
    table_mappings = [
        ('TechReformApp_cpu', 'ProductsApp_cpu'),
        ('TechReformApp_cooler', 'ProductsApp_cooler'),
        ('TechReformApp_motherboard', 'ProductsApp_motherboard'),
        ('TechReformApp_ram', 'ProductsApp_ram'),
        ('TechReformApp_ssd', 'ProductsApp_ssd'),
        ('TechReformApp_hdd', 'ProductsApp_hdd'),
        ('TechReformApp_gpu', 'ProductsApp_gpu'),
        ('TechReformApp_powersupply', 'ProductsApp_powersupply'),
        ('TechReformApp_casing', 'ProductsApp_casing'),
        ('TechReformApp_monitor', 'ProductsApp_monitor'),
        ('TechReformApp_keyboard', 'ProductsApp_keyboard'),
        ('TechReformApp_mouse', 'ProductsApp_mouse'),
        ('TechReformApp_headphone', 'ProductsApp_headphone'),
    ]

    # Get all existing tables based on database vendor
    if db_vendor == 'sqlite':
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [row[0] for row in cursor.fetchall()]
    elif db_vendor == 'postgresql':
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """)
        existing_tables = [row[0] for row in cursor.fetchall()]
    else:
        # For other databases, skip this migration
        return

    for source_table, dest_table in table_mappings:
        if source_table in existing_tables and dest_table in existing_tables:
            try:
                # Get column information based on database vendor
                if db_vendor == 'sqlite':
                    # Get column names from source table
                    cursor.execute(f"PRAGMA table_info({source_table})")
                    source_columns = [row[1] for row in cursor.fetchall()]

                    # Get column names from destination table
                    cursor.execute(f"PRAGMA table_info({dest_table})")
                    dest_columns_info = cursor.fetchall()
                    dest_columns = [row[1] for row in dest_columns_info]
                elif db_vendor == 'postgresql':
                    # Get column names from source table
                    cursor.execute(f"""
                        SELECT column_name
                        FROM information_schema.columns
                        WHERE table_name = '{source_table}'
                        AND table_schema = 'public'
                    """)
                    source_columns = [row[0] for row in cursor.fetchall()]

                    # Get column names from destination table
                    cursor.execute(f"""
                        SELECT column_name, data_type, is_nullable
                        FROM information_schema.columns
                        WHERE table_name = '{dest_table}'
                        AND table_schema = 'public'
                    """)
                    dest_columns_info = cursor.fetchall()
                    dest_columns = [row[0] for row in dest_columns_info]

                # Find columns that exist in both tables
                common_columns = [col for col in source_columns if col in dest_columns]
                common_columns_str = ', '.join(common_columns)

                # Clear destination table
                cursor.execute(f"DELETE FROM {dest_table}")

                # Prepare the INSERT statement with explicit column names
                if common_columns:
                    cursor.execute(f"INSERT INTO {dest_table} ({common_columns_str}) SELECT {common_columns_str} FROM {source_table}")

                # Set default values for new required columns (SQLite only)
                if db_vendor == 'sqlite':
                    required_columns = [(row[1], row[2]) for row in dest_columns_info
                                       if row[3] == 1 and row[1] not in common_columns]

                    if required_columns:
                        # Get all records that were just inserted
                        cursor.execute(f"SELECT id FROM {dest_table}")
                        inserted_ids = [row[0] for row in cursor.fetchall()]

                        for id_val in inserted_ids:
                            # Set defaults for each new required column
                            for col_name, col_type in required_columns:
                                if col_type.lower() in ('integer', 'int'):
                                    default_val = 0
                                elif col_type.lower() in ('real', 'float'):
                                    default_val = 0.0
                                elif col_type.lower() == 'boolean':
                                    default_val = 1  # True
                                else:
                                    default_val = ''

                                cursor.execute(f"UPDATE {dest_table} SET {col_name} = ? WHERE id = ?",
                                              (default_val, id_val))

                # Data copied successfully from {source_table} to {dest_table}
            except Exception:
                # Error copying data: silently continue
                pass


class Migration(migrations.Migration):
    dependencies = [
        ('ProductsApp', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(copy_data, migrations.RunPython.noop),
    ]