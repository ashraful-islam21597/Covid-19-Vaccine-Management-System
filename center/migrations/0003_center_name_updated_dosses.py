# Generated by Django 2.0.1 on 2021-08-10 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('center', '0002_center_name_doss_per_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='center_name',
            name='updated_dosses',
            field=models.IntegerField(default=0),
        ),
    ]
