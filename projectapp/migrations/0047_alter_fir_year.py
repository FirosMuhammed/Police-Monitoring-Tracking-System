# Generated by Django 5.1.4 on 2025-02-17 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectapp', '0046_alter_fir_content_fir_alter_fir_details_case_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fir',
            name='year',
            field=models.IntegerField(),
        ),
    ]
