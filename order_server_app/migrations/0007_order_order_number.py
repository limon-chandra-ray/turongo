# Generated by Django 5.0.2 on 2024-02-28 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_server_app', '0006_order_total_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_number',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
