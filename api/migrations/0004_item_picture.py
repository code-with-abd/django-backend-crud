# Generated by Django 5.1.2 on 2024-11-01 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='item_pictures/'),
        ),
    ]
