# Generated by Django 5.0.7 on 2024-12-15 09:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='proof',
            field=models.ImageField(blank=True, null=True, upload_to='payment_proofs/', verbose_name='Payment Proof'),
        ),
        migrations.AddField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('success', 'Success')], default='pending', max_length=10, verbose_name='Payment Status'),
        ),
        migrations.CreateModel(
            name='PaymentProof',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proof', models.ImageField(upload_to='payment_proof/', verbose_name='Proof of Payment')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, verbose_name='Uploaded At')),
                ('payment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment_proof', to='Payment.payment', verbose_name='Payment')),
            ],
            options={
                'verbose_name_plural': 'Payment Proof',
                'ordering': ['-uploaded_at'],
            },
        ),
    ]