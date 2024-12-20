# Generated by Django 5.0.2 on 2024-02-23 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server_object_app', '0002_rename_slide_iamge_slider_slide_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slider',
            name='display_type',
        ),
        migrations.AddField(
            model_name='slider',
            name='slide_link',
            field=models.URLField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='slider',
            name='slide_image',
            field=models.FileField(upload_to='slide-image/'),
        ),
    ]
