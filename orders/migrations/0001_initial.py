# Generated by Django 3.1.3 on 2020-12-05 09:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customer_id', models.PositiveBigIntegerField(primary_key=True, serialize=False, verbose_name='Customer ID')),
                ('is_vip', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('shop_id', models.TextField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.PositiveBigIntegerField(primary_key=True, serialize=False, verbose_name='Product ID')),
                ('stock_pcs', models.IntegerField(verbose_name='Stock PCS')),
                ('price', models.IntegerField(verbose_name='Price')),
                ('vip', models.BooleanField()),
                ('shop_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='orders.shop')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.PositiveBigIntegerField(primary_key=True, serialize=False, verbose_name='Order ID')),
                ('qty', models.IntegerField(verbose_name='Quantity')),
                ('price', models.IntegerField(verbose_name='Price')),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='orders.customer')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='orders.product')),
                ('shop_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='orders.shop')),
            ],
        ),
    ]
