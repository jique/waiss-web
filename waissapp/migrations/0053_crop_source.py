# Generated by Django 3.0.8 on 2020-09-30 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waissapp', '0052_auto_20200924_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='crop',
            name='source',
            field=models.CharField(max_length=30, null=True, verbose_name='Data Source'),
        ),
    ]
