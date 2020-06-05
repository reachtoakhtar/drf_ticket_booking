# Generated by Django 3.0.3 on 2020-02-09 15:54

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Row',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('no_of_seats', models.IntegerField()),
                ('aisle_seats', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
            ],
        ),
        migrations.CreateModel(
            name='Screen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024, unique=True)),
                ('rows', models.ManyToManyField(blank=True, to='booking.Row')),
            ],
        ),
        migrations.CreateModel(
            name='Reserve',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seats_reserved', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('row', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='row_reserve', to='booking.Row')),
                ('screen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='screen_reserve', to='booking.Screen')),
            ],
        ),
    ]