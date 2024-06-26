# Generated by Django 3.0.8 on 2020-08-06 05:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('waissapp', '0025_auto_20200806_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='moisturecontent',
            name='farm_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.Farm'),
        ),
        migrations.AddField(
            model_name='sensornumber',
            name='farm_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.Farm'),
        ),
        migrations.AlterField(
            model_name='sensornumber',
            name='fieldunit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.FieldUnit'),
        ),
    ]
