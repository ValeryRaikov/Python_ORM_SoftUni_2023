# Generated by Django 4.2.4 on 2023-11-09 08:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_student'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='gare',
            new_name='grade',
        ),
    ]
