# Generated by Django 5.0.2 on 2024-02-20 12:45

import django.db.models.deletion
import django_ckeditor_5.fields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product_accessorie_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=150)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='RootCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rc_name', models.CharField(max_length=150, unique=True)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='RootCategoryThree',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rc_three_name', models.CharField(max_length=150)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('p_id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('p_name', models.CharField(max_length=250)),
                ('p_price', models.BigIntegerField()),
                ('p_offer_price', models.BigIntegerField(blank=True, null=True)),
                ('p_offer', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('p_status', models.BooleanField(default=False)),
                ('p_description', django_ckeditor_5.fields.CKEditor5Field()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('p_brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product_accessorie_app.pbrand')),
                ('p_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_server_app.category')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_image', models.FileField(upload_to='product/')),
                ('pimage_type', models.CharField(max_length=50)),
                ('pimage_priority', models.IntegerField(blank=True, default=0, null=True)),
                ('image_status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_images', to='product_server_app.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.BigIntegerField(blank=True, default=0, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('p_size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_accessorie_app.psize')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_sizes', to='product_server_app.product')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='root_category_three',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_server_app.rootcategorythree'),
        ),
        migrations.CreateModel(
            name='RootCategoryTwo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rc_two_name', models.CharField(max_length=150)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('root_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_server_app.rootcategory')),
            ],
        ),
        migrations.AddField(
            model_name='rootcategorythree',
            name='root_category_two',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_server_app.rootcategorytwo'),
        ),
    ]