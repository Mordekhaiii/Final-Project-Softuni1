# Generated by Django 5.0.7 on 2024-12-14 18:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Riwayat_transaksi', '0001_initial'),
        ('orders', '0004_alter_order_total_price'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='transactionhistory',
            old_name='created_at',
            new_name='date',
        ),
        migrations.AddField(
            model_name='transactionhistory',
            name='brand',
            field=models.CharField(default='Unknown Brand', max_length=100),
        ),
        migrations.AddField(
            model_name='transactionhistory',
            name='payment_method',
            field=models.CharField(choices=[('Cash', 'Cash'), ('QRIS', 'QRIS')], default='Cash', max_length=50),
        ),
        migrations.AlterField(
            model_name='transactionhistory',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.product'),
        ),
        migrations.AlterField(
            model_name='transactionhistory',
            name='quantity',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='transactionhistory',
            name='total_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='transactionhistory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
