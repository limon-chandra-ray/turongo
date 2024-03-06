# Generated by Django 5.0.2 on 2024-02-23 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_type', models.CharField(max_length=50)),
                ('slide_iamge', models.FileField(upload_to='slide-image')),
                ('slide_status', models.BooleanField(default=False)),
                ('slide_priority', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]