# Generated by Django 3.0.8 on 2020-07-08 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waissapp', '0004_auto_20200708_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fieldunit',
            name='name',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]