# Generated by Django 3.0.8 on 2020-07-08 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('waissapp', '0002_auto_20200708_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='calibrationconstant',
            name='sensor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.SensorNumber', verbose_name='Sensor Name'),
        ),
        migrations.AlterField(
            model_name='calibrationconstant',
            name='farm_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.Farm', verbose_name='Farm Name'),
        ),
        migrations.AlterField(
            model_name='calibrationconstant',
            name='soiltype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.Soil', verbose_name='Soil Type'),
        ),
        migrations.AlterField(
            model_name='crop',
            name='depletionfactor',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True, verbose_name='Depletion Factor'),
        ),
        migrations.AlterField(
            model_name='crop',
            name='growingperiod',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=5, null=True, verbose_name='Growing Period, days'),
        ),
        migrations.AlterField(
            model_name='crop',
            name='mad',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True, verbose_name='Management Allowable Deficit'),
        ),
        migrations.AlterField(
            model_name='farm',
            name='farm_name',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='farmsummaries',
            name='calib_coeff_a',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=20, null=True, verbose_name=' a'),
        ),
        migrations.AlterField(
            model_name='farmsummaries',
            name='calib_coeff_b',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=20, null=True, verbose_name=' b'),
        ),
        migrations.AlterField(
            model_name='farmsummaries',
            name='calib_coeff_c',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=20, null=True, verbose_name=' c'),
        ),
        migrations.AlterField(
            model_name='farmsummaries',
            name='calib_coeff_d',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=20, null=True, verbose_name=' d'),
        ),
        migrations.AlterField(
            model_name='farmsummaries',
            name='calib_coeff_m',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=20, null=True, verbose_name=' m'),
        ),
        migrations.AlterField(
            model_name='farmsummaries',
            name='coeff_a',
            field=models.DecimalField(decimal_places=4, max_digits=5, null=True, verbose_name=' a'),
        ),
        migrations.AlterField(
            model_name='farmsummaries',
            name='coeff_b',
            field=models.DecimalField(decimal_places=3, max_digits=4, null=True, verbose_name=' b'),
        ),
        migrations.AlterField(
            model_name='farmsummaries',
            name='coeff_c',
            field=models.DecimalField(decimal_places=0, max_digits=1, null=True, verbose_name=' c'),
        ),
        migrations.AlterField(
            model_name='farmsummaries',
            name='coeff_f',
            field=models.DecimalField(decimal_places=2, max_digits=4, null=True, verbose_name=' f'),
        ),
        migrations.AlterField(
            model_name='farmsummaries',
            name='coeff_g',
            field=models.DecimalField(decimal_places=7, max_digits=9, null=True, verbose_name=' g'),
        ),
        migrations.AlterField(
            model_name='fieldunit',
            name='farm_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.Farm', unique=True),
        ),
        migrations.AlterField(
            model_name='fieldunit',
            name='name',
            field=models.CharField(blank=True, max_length=25, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='intakefamily',
            name='coeff_a',
            field=models.DecimalField(decimal_places=4, max_digits=5, null=True, verbose_name=' a'),
        ),
        migrations.AlterField(
            model_name='intakefamily',
            name='coeff_b',
            field=models.DecimalField(decimal_places=3, max_digits=4, null=True, verbose_name=' b'),
        ),
        migrations.AlterField(
            model_name='intakefamily',
            name='coeff_c',
            field=models.DecimalField(decimal_places=0, max_digits=1, null=True, verbose_name=' c'),
        ),
        migrations.AlterField(
            model_name='intakefamily',
            name='coeff_f',
            field=models.DecimalField(decimal_places=2, max_digits=4, null=True, verbose_name=' f'),
        ),
        migrations.AlterField(
            model_name='intakefamily',
            name='coeff_g',
            field=models.DecimalField(decimal_places=7, max_digits=9, null=True, verbose_name=' g'),
        ),
        migrations.AlterField(
            model_name='sensornumber',
            name='farm_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.Farm'),
        ),
        migrations.AlterField(
            model_name='sensornumber',
            name='name',
            field=models.CharField(max_length=30, null=True, unique=True, verbose_name='Sensor Name'),
        ),
    ]
