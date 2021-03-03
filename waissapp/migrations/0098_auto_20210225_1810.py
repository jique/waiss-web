# Generated by Django 3.0.8 on 2021-02-25 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waissapp', '0097_auto_20210223_1510'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='irrigationparameters',
            name='flow_rate_per_strip',
        ),
        migrations.RemoveField(
            model_name='irrigationparameters',
            name='total_flow_rate',
        ),
        migrations.AddField(
            model_name='irrigationparameters',
            name='fcoarser_rate_per_strip',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=20, null=True, verbose_name='Fcoarser rate per border strip (lps)'),
        ),
        migrations.AddField(
            model_name='irrigationparameters',
            name='total_fcoarser_rate',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=20, null=True, verbose_name='Total fcoarser rate (lps)'),
        ),
        migrations.AddField(
            model_name='soil',
            name='intake_family',
            field=models.CharField(blank=True, choices=[('clay_005', 'clay_005'), ('clay_01', 'clay_01'), ('clay_015', 'clay_015'), ('clay loam_02', 'clay loam_02'), ('clay loam_025', 'clay loam_025'), ('clay loam_03', 'clay loam_03'), ('silty_035', 'silty_035'), ('silty_04', 'silty_04'), ('silty loam_045', 'silty loam_045'), ('silty loam_05', 'silty loam_05'), ('silty loam_06', 'silty loam_06'), ('silty loam_07', 'silty loam_07'), ('sandy loam_08', 'sandy loam_08'), ('sandy loam_09', 'sandy loam_09'), ('sandy loam_10', 'sandy loam_10'), ('sandy_15', 'sandy_15'), ('sandy_20', 'sandy_20')], max_length=30, null=True, verbose_name='Intake Family'),
        ),
        migrations.AlterField(
            model_name='crop',
            name='kc_mid',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Kc (medium)'),
        ),
        migrations.AlterField(
            model_name='crop',
            name='mad',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True, verbose_name='Management Alcoarserable Deficit'),
        ),
        migrations.AlterField(
            model_name='crop',
            name='root_growth_model',
            field=models.CharField(blank=True, choices=[('Borg-Grimes Model', 'Borg-Grimes Model'), ('User-Defined', 'User-Definerd'), ('Inverse Kc', 'Inverse Kc')], max_length=30, null=True, verbose_name='Root Growth Model'),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='depth',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Depth, m'),
        ),
    ]
