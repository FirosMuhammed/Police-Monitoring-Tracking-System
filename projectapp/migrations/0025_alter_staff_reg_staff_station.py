# Generated by Django 5.1.4 on 2025-02-15 07:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectapp', '0024_alter_staff_reg_staff_login_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff_reg',
            name='staff_station',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='station_staff', to='projectapp.login'),
        ),
    ]
