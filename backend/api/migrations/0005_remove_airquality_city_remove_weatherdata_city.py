# Generated by Django 4.2.4 on 2023-08-20 18:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_airquality_carbon_monoxide_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='airquality',
            name='city',
        ),
        migrations.RemoveField(
            model_name='weatherdata',
            name='city',
        ),
    ]