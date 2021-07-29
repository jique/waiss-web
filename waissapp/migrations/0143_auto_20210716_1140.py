# Generated by Django 3.0.8 on 2021-07-16 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waissapp', '0142_auto_20210713_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farm',
            name='lat',
            field=models.DecimalField(blank='True', decimal_places=4, max_digits=6, null='True', verbose_name='Latitude'),
        ),
        migrations.AlterField(
            model_name='farm',
            name='long',
            field=models.DecimalField(blank='True', decimal_places=4, max_digits=7, null='True', verbose_name='Longitude'),
        ),
    ]
