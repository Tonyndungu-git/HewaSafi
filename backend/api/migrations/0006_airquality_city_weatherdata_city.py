# Generated by Django 4.2.4 on 2023-08-20 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_remove_airquality_city_remove_weatherdata_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='airquality',
            name='city',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='weatherdata',
            name='city',
            field=models.CharField(default='', max_length=100),
        ),
    ]
