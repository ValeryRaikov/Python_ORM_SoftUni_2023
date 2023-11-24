# Generated by Django 4.2.4 on 2023-11-11 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('main_app', '0001_initial'), ('main_app', '0002_artifact'), ('main_app', '0003_location'), ('main_app', '0004_car'), ('main_app', '0005_taskencoder'), ('main_app', '0006_rename_taskencoder_task'), ('main_app', '0007_hotelroom'), ('main_app', '0008_alter_hotelroom_room_type'), ('main_app', '0009_character')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('species', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Artifact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
                ('origin', models.CharField(max_length=70)),
                ('age', models.PositiveIntegerField()),
                ('description', models.TextField()),
                ('is_magical', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('region', models.CharField(max_length=50)),
                ('population', models.PositiveIntegerField()),
                ('description', models.TextField()),
                ('is_capital', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=40)),
                ('year', models.PositiveIntegerField()),
                ('color', models.CharField(max_length=40)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price_with_discount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25)),
                ('description', models.TextField()),
                ('due_date', models.DateField()),
                ('is_finished', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='HotelRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.PositiveIntegerField()),
                ('room_type', models.CharField(choices=[('Standard', 'Standard'), ('Deluxe', 'Suite'), ('Suite', 'Suite')], max_length=50)),
                ('capacity', models.PositiveIntegerField()),
                ('amenities', models.TextField()),
                ('price_per_night', models.DecimalField(decimal_places=2, max_digits=8)),
                ('is_reserved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('class_name', models.CharField(choices=[('Mage', 'Mage'), ('Warrior', 'Warrior'), ('Assassin', 'Assassin'), ('Scout', 'Scout')], max_length=20)),
                ('level', models.PositiveIntegerField()),
                ('strength', models.PositiveIntegerField()),
                ('dexterity', models.PositiveIntegerField()),
                ('intelligence', models.PositiveIntegerField()),
                ('hit_points', models.PositiveIntegerField()),
                ('inventory', models.TextField()),
            ],
        ),
    ]
