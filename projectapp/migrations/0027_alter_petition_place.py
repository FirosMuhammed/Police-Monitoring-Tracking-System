# Generated by Django 5.1.4 on 2025-02-15 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectapp', '0026_alter_police_station_login_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petition',
            name='place',
            field=models.CharField(max_length=100),
        ),
    ]
