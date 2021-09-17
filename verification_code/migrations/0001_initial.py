# Generated by Django 2.0.1 on 2021-09-17 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('citizen', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='code',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, max_length=6)),
                ('registered_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='citizen.people')),
            ],
        ),
    ]