# Generated by Django 4.2.4 on 2023-11-02 13:45
import django
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False
        ),
        migrations.AddField(
            model_name='product',
            name='last_edited_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
