# Generated by Django 3.0.8 on 2020-07-14 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waissapp', '0012_auto_20200709_1525'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='crop',
            name='farm_name',
        ),
        migrations.RemoveField(
            model_name='crop',
            name='fieldunit',
        ),
        migrations.RemoveField(
            model_name='intakefamily',
            name='farm_name',
        ),
        migrations.RemoveField(
            model_name='intakefamily',
            name='fieldunit',
        ),
        migrations.AlterField(
            model_name='farm',
            name='farm_name',
            field=models.CharField(default=False, max_length=20),
            preserve_default=False,
        ),
    ]