# Generated by Django 3.0.8 on 2021-01-28 07:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('waissapp', '0083_auto_20210128_1513'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fieldunit',
            old_name='fieldunit_number',
            new_name='number',
        ),
    ]