# Generated by Django 3.0.8 on 2020-08-13 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('waissapp', '0027_auto_20200812_1830'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='drippara',
            name='optimum_emitter_spacing',
        ),
        migrations.RemoveField(
            model_name='furrowpara',
            name='p_adjusted',
        ),
        migrations.RemoveField(
            model_name='sprinklerpara',
            name='bln_operating_pressure',
        ),
        migrations.RemoveField(
            model_name='sprinklerpara',
            name='discharge_coefficient',
        ),
        migrations.RemoveField(
            model_name='sprinklerpara',
            name='nozzle_dia',
        ),
        migrations.RemoveField(
            model_name='sprinklerpara',
            name='operating_pressure',
        ),
        migrations.AlterField(
            model_name='basinpara',
            name='farm_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.Farm', verbose_name='Farm'),
        ),
        migrations.AlterField(
            model_name='basinpara',
            name='fieldunit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.FieldUnit', verbose_name='Field Unit'),
        ),
        migrations.AlterField(
            model_name='drippara',
            name='EU',
            field=models.DecimalField(decimal_places=3, max_digits=3, null=True, verbose_name='Design Emission Uniformity'),
        ),
        migrations.AlterField(
            model_name='drippara',
            name='farm_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.Farm', verbose_name='Farm'),
        ),
        migrations.AlterField(
            model_name='drippara',
            name='fieldunit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.FieldUnit', verbose_name='Field Unit'),
        ),
        migrations.AlterField(
            model_name='sprinklerpara',
            name='farm_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.Farm', verbose_name='Farm'),
        ),
        migrations.AlterField(
            model_name='sprinklerpara',
            name='fieldunit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.FieldUnit', verbose_name='Field Unit'),
        ),
    ]
