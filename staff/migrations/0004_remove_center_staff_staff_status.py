# Generated by Django 2.0.1 on 2021-08-19 06:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0003_auto_20210819_1031'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='center_staff',
            name='staff_status',
        ),
    ]
