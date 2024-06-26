# Generated by Django 3.0.8 on 2020-07-08 07:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('waissapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='calibrationconstant',
            name='soiltype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.Soil'),
        ),
        migrations.AlterField(
            model_name='calibrationconstant',
            name='farm_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.Farm'),
        ),
        migrations.AlterField(
            model_name='calibrationconstant',
            name='fieldunit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.FieldUnit', verbose_name='Field Unit Name'),
        ),
    ]
