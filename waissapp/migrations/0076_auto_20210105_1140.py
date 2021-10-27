# Generated by Django 3.0.8 on 2021-01-05 03:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('waissapp', '0075_auto_20201209_1513'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fieldunit',
            old_name='fieldunitnumber',
            new_name='mobilenumber',
        ),
        migrations.AlterField(
            model_name='farm',
            name='fieldunit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.FieldUnit', verbose_name='Field Unit'),
        ),
    ]