# Generated by Django 5.0.2 on 2024-03-30 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_server_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='full_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]