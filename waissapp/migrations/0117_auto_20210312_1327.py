# Generated by Django 3.0.8 on 2021-03-12 05:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('waissapp', '0116_auto_20210309_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crop',
            name='root_growth_model',
            field=models.CharField(choices=[('Borg-Grimes Model', 'Borg-Grimes Model'), ('User-Defined', 'User-Defined'), ('Inverse Kc', 'Inverse Kc')], max_length=30, null=True, verbose_name='Root Growth Model'),
        ),
        migrations.AlterField(
            model_name='rainfall',
            name='timestamp',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Date/Time Sent'),
        ),
        migrations.AlterField(
            model_name='waissystems',
            name='calib',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.CalibrationConstant', verbose_name='Calibration Equation'),
        ),
        migrations.AlterField(
            model_name='waissystems',
            name='crop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.Crop'),
        ),
        migrations.AlterField(
            model_name='waissystems',
            name='farm',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.Farm', verbose_name='Farm'),
        ),
        migrations.AlterField(
            model_name='waissystems',
            name='farm_manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.Personnel', verbose_name='Farm Manager'),
        ),
        migrations.AlterField(
            model_name='waissystems',
            name='fieldunit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.FieldUnit', verbose_name='Field Unit'),
        ),
        migrations.AlterField(
            model_name='waissystems',
            name='irrigation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.IrrigationParameters', verbose_name='Irrigation System'),
        ),
        migrations.AlterField(
            model_name='waissystems',
            name='soil',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.Soil'),
        ),
    ]
