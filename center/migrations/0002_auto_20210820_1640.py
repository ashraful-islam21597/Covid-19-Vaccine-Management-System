# Generated by Django 2.0.1 on 2021-08-20 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('center', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='center_name',
            name='pending_doss_center',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='center_name',
            name='total_doss_center',
            field=models.IntegerField(default=0),
        ),
    ]