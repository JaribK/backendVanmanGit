# Generated by Django 5.0.3 on 2024-05-16 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_logged_in',
            field=models.BooleanField(default=False, verbose_name='logged in'),
        ),
    ]
