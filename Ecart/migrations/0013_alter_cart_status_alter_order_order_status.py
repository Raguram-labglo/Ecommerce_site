# Generated by Django 4.1.2 on 2022-11-03 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecart', '0012_alter_cart_status_alter_order_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='status',
            field=models.IntegerField(choices=[('pending', 'pending'), ('success', 'success'), ('failed', 'failed')], default=1),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.IntegerField(choices=[('pending', 'pending'), ('success', 'success'), ('failed', 'failed')], default='pending'),
        ),
    ]
