# Generated by Django 2.0.1 on 2021-08-20 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('City', '0004_auto_20210820_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='number_of_center',
            field=models.IntegerField(default=0),
        ),
    ]
