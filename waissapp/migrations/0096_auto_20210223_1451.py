# Generated by Django 3.0.8 on 2021-02-23 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waissapp', '0095_auto_20210217_1510'),
    ]

    operations = [
        migrations.DeleteModel(
            name='IntakeFamily',
        ),
        migrations.RenameField(
            model_name='calibrationconstant',
            old_name='calib_coeff_a',
            new_name='coeff_a',
        ),
        migrations.RenameField(
            model_name='calibrationconstant',
            old_name='calib_coeff_b',
            new_name='coeff_b',
        ),
        migrations.RenameField(
            model_name='calibrationconstant',
            old_name='calib_coeff_c',
            new_name='coeff_c',
        ),
        migrations.RenameField(
            model_name='calibrationconstant',
            old_name='calib_coeff_d',
            new_name='coeff_d',
        ),
        migrations.RenameField(
            model_name='calibrationconstant',
            old_name='calib_coeff_m',
            new_name='coeff_m',
        ),
        migrations.AlterField(
            model_name='crop',
            name='growingperiod',
            field=models.IntegerField(blank=True, null=True, verbose_name='Growing Period, days'),
        ),
        migrations.AlterField(
            model_name='irrigationparameters',
            name='discharge',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='Unit Discharge (lps)'),
        ),
    ]
