# Generated by Django 3.0.8 on 2020-07-09 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waissapp', '0007_auto_20200708_1811'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dripcomp',
            name='Fn',
        ),
        migrations.RemoveField(
            model_name='dripcomp',
            name='Mc1',
        ),
        migrations.RemoveField(
            model_name='dripcomp',
            name='Mc2',
        ),
        migrations.RemoveField(
            model_name='dripcomp',
            name='Mc3',
        ),
        migrations.RemoveField(
            model_name='dripcomp',
            name='McToIrrigate',
        ),
        migrations.RemoveField(
            model_name='dripcomp',
            name='Ta',
        ),
        migrations.RemoveField(
            model_name='dripcomp',
            name='Ti',
        ),
        migrations.RemoveField(
            model_name='dripcomp',
            name='Tn',
        ),
        migrations.RemoveField(
            model_name='dripcomp',
            name='Tt',
        ),
        migrations.RemoveField(
            model_name='dripcomp',
            name='appeff',
        ),
        migrations.RemoveField(
            model_name='dripcomp',
            name='discharge',
        ),
        migrations.RemoveField(
            model_name='dripcomp',
            name='eff_adv_ratio',
        ),
        migrations.RemoveField(
            model_name='dripcomp',
            name='length',
        ),
        migrations.AddField(
            model_name='dripcomp',
            name='EU',
            field=models.DecimalField(decimal_places=2, max_digits=3, null=True, verbose_name='Design Emission Uniformity'),
        ),
        migrations.AddField(
            model_name='dripcomp',
            name='ave_emitter_discharge',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Average emitter discharge (lps)'),
        ),
        migrations.AddField(
            model_name='dripcomp',
            name='ave_peak_daily_transpiration',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Average Peak Daily Transpiration Rate'),
        ),
        migrations.AddField(
            model_name='dripcomp',
            name='bln_compute_EU',
            field=models.BooleanField(default=True, verbose_name='Design Emission Uniformity unknown, compute!'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dripcomp',
            name='bln_compute_emitter_coeff',
            field=models.BooleanField(default=True, verbose_name='Emitter coefficient unknown, compute!'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dripcomp',
            name='bln_prefers_irrig_interval',
            field=models.BooleanField(default=True, verbose_name='Do you have preffered irrigation interval?'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dripcomp',
            name='bln_pw_between_33_and_50',
            field=models.BooleanField(default=True, verbose_name='Is the Percent Wetted Perimeter between 33 to 50 percent?'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dripcomp',
            name='bln_single_lateral',
            field=models.BooleanField(default=True, verbose_name='Is your system a Single Straight Lateral type?'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dripcomp',
            name='emitter_coeff',
            field=models.DecimalField(decimal_places=2, help_text='input emitter coefficient if known', max_digits=5, null=True, verbose_name='Emitter coefficient'),
        ),
        migrations.AddField(
            model_name='dripcomp',
            name='emitter_spacing',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Emitter Spacing (m)'),
        ),
        migrations.AddField(
            model_name='dripcomp',
            name='emitters_per_plant',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='No. of Emitters per Plant'),
        ),
        migrations.AddField(
            model_name='dripcomp',
            name='gross_app_depth',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Gross Application Depth (mm)'),
        ),
        migrations.AddField(
            model_name='dripcomp',
            name='gross_volume_required_per_plant',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Gross Volume Required per Plant (l)'),
        ),
        migrations.AddField(
            model_name='dripcomp',
            name='irrigation_interval',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Irrigation Interval (days)'),
        ),
        migrations.AddField(
            model_name='dripcomp',
            name='irrigation_period',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Irrigation Peiod (mins)'),
        ),
        migrations.AddField(
            model_name='dripcomp',
            name='min_emitter_discharge',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Average emitter discharge (lps)'),
        ),
        migrations.AddField(
            model_name='dripcomp',
            name='net_app_depth',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Net Application Depth (mm)'),
        ),
        migrations.AddField(
            model_name='dripcomp',
            name='optimum_emitter_spacing',
            field=models.DecimalField(decimal_places=2, help_text='Leave blank if wetted width is filled out.', max_digits=5, null=True, verbose_name='Optimum Emitter Spacing (m)'),
        ),
        migrations.AddField(
            model_name='dripcomp',
            name='peak_ETo',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Peak Evapotranspiration (mm)'),
        ),
        migrations.AddField(
            model_name='dripcomp',
            name='percent_shaded',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Percent Shaded (%)'),
        ),
        migrations.AddField(
            model_name='dripcomp',
            name='percent_wetted_area',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Percent Wetted Diameter (%)'),
        ),
        migrations.AddField(
            model_name='dripcomp',
            name='plant_spacing',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Plant spacing (m)'),
        ),
        migrations.AddField(
            model_name='dripcomp',
            name='row_spacing',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Row spacing (m)'),
        ),
        migrations.AddField(
            model_name='dripcomp',
            name='transpiration_requirement',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Transpiration Requirement (?)'),
        ),
        migrations.AddField(
            model_name='dripcomp',
            name='wetted_dia',
            field=models.DecimalField(decimal_places=2, help_text='Leave blank if wetted width is filled out.', max_digits=5, null=True, verbose_name='Wetted diameter (m)'),
        ),
        migrations.AddField(
            model_name='dripcomp',
            name='wetted_width',
            field=models.DecimalField(decimal_places=2, help_text='Leave blank if wetted portion is circular.', max_digits=5, null=True, verbose_name='Wetted width (m)'),
        ),
        migrations.AlterField(
            model_name='farmsummaries',
            name='As',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Apparent Specific Density, % MCv'),
        ),
        migrations.AlterField(
            model_name='farmsummaries',
            name='McToIrrig',
            field=models.DecimalField(decimal_places=2, max_digits=4, null=True, verbose_name='MC to Irrigate, % MCv'),
        ),
        migrations.AlterField(
            model_name='farmsummaries',
            name='fc',
            field=models.DecimalField(decimal_places=2, max_digits=4, null=True, verbose_name='Field Capacity, % MCv'),
        ),
        migrations.AlterField(
            model_name='farmsummaries',
            name='pwp',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Permanent Wilting Point, % MCv'),
        ),
    ]
