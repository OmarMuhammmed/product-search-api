from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('products', '0003_alter_product_options'),
    ]

    operations = [
        migrations.RunSQL(
            'CREATE EXTENSION IF NOT EXISTS pg_trgm;',
            'DROP EXTENSION IF EXISTS pg_trgm;'
        ),
    ] 