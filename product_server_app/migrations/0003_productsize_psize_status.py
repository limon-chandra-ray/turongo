# Generated by Django 5.0.2 on 2024-03-06 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_server_app', '0002_productask'),
    ]

    operations = [
        migrations.AddField(
            model_name='productsize',
            name='psize_status',
            field=models.BooleanField(default=True),
        ),
    ]
