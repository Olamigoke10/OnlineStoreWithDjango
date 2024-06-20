# Generated by Django 5.0.6 on 2024-06-20 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant_menu', '0011_remove_video_video_url_video_video_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='menu_cards/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
