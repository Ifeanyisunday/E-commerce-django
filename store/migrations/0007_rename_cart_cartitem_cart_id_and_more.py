# Generated by Django 5.1.3 on 2024-11-07 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_cartitem_cart'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='cart',
            new_name='cart_id',
        ),
        migrations.RenameField(
            model_name='cartitem',
            old_name='product',
            new_name='product_id',
        ),
    ]