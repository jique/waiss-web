# Generated by Django 3.0.8 on 2020-08-06 05:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('waissapp', '0024_auto_20200730_1330'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basincomp',
            name='basin_length',
        ),
        migrations.RemoveField(
            model_name='basincomp',
            name='basin_name',
        ),
        migrations.RemoveField(
            model_name='basincomp',
            name='discharge',
        ),
        migrations.RemoveField(
            model_name='basincomp',
            name='ea',
        ),
        migrations.RemoveField(
            model_name='basincomp',
            name='eff_adv_ratio',
        ),
        migrations.RemoveField(
            model_name='bordercomp',
            name='area_slope',
        ),
        migrations.RemoveField(
            model_name='bordercomp',
            name='border_name',
        ),
        migrations.RemoveField(
            model_name='bordercomp',
            name='border_width',
        ),
        migrations.RemoveField(
            model_name='bordercomp',
            name='discharge',
        ),
        migrations.RemoveField(
            model_name='bordercomp',
            name='ea',
        ),
        migrations.RemoveField(
            model_name='bordercomp',
            name='flow_rate_per_strip',
        ),
        migrations.RemoveField(
            model_name='bordercomp',
            name='mannings_coeff',
        ),
        migrations.RemoveField(
            model_name='bordercomp',
            name='num_of_border_strips',
        ),
        migrations.RemoveField(
            model_name='bordercomp',
            name='total_flow_rate',
        ),
        migrations.RemoveField(
            model_name='dripcomp',
            name='EU',
        ),
        migrations.RemoveField(
            model_name='dripcomp',
            name='bln_single_lateral',
        ),
        migrations.RemoveField(
            model_name='dripcomp',
            name='emitter_spacing',
        ),
        migrations.RemoveField(
            model_name='dripcomp',
            name='emitters_per_plant',
        ),
        migrations.RemoveField(
            model_name='dripcomp',
            name='irrigation_interval',
        ),
        migrations.RemoveField(
            model_name='dripcomp',
            name='name',
        ),
        migrations.RemoveField(
            model_name='dripcomp',
            name='optimum_emitter_spacing',
        ),
        migrations.RemoveField(
            model_name='dripcomp',
            name='plant_spacing',
        ),
        migrations.RemoveField(
            model_name='dripcomp',
            name='row_spacing',
        ),
        migrations.RemoveField(
            model_name='dripcomp',
            name='wetted_dia',
        ),
        migrations.RemoveField(
            model_name='dripcomp',
            name='wetted_width',
        ),
        migrations.RemoveField(
            model_name='furrowcomp',
            name='area_slope',
        ),
        migrations.RemoveField(
            model_name='furrowcomp',
            name='bln_furrow_type',
        ),
        migrations.RemoveField(
            model_name='furrowcomp',
            name='discharge',
        ),
        migrations.RemoveField(
            model_name='furrowcomp',
            name='name',
        ),
        migrations.RemoveField(
            model_name='furrowcomp',
            name='p_adjusted',
        ),
        migrations.AlterField(
            model_name='dripcomp',
            name='min_emitter_discharge',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Minimum emitter discharge (lps)'),
        ),
        migrations.CreateModel(
            name='SprinklerPara',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, null=True, verbose_name='System Name')),
                ('farm_area', models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Farm area (sq.m)')),
                ('area_irrigated_at_a_time', models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Area irrigated at a time (sq.m)')),
                ('lateral_spacing', models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Lateral spacing (m)')),
                ('sprinkler_spacing', models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Sprinkler spacing (m)')),
                ('num_of_sprinklers', models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Number of sprinklers')),
                ('ea', models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Application Efficiency')),
                ('bln_operating_pressure', models.BooleanField(verbose_name='Is the operating pressure known?')),
                ('operating_pressure', models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Operating Pressure (kPa)')),
                ('nozzle_dia', models.DecimalField(decimal_places=2, help_text='Fill-out only if operating pressure is known.', max_digits=5, null=True, verbose_name='Nozzle diameter (mm)')),
                ('discharge_coefficient', models.DecimalField(decimal_places=2, help_text='Fill-out only if operating pressure is known.', max_digits=5, null=True, verbose_name='Discharge Coefficient')),
                ('sprinkler_discharge', models.DecimalField(decimal_places=2, help_text='Fill-out if operating pressure is unknown.', max_digits=5, null=True, verbose_name='Sprinkler Discharge (lps)')),
                ('farm_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.Farm')),
                ('fieldunit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.FieldUnit', verbose_name='Field unit')),
            ],
            options={
                'verbose_name_plural': 'Irrigation System: Sprinkler',
            },
        ),
        migrations.CreateModel(
            name='FurrowPara',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, null=True, verbose_name='System Name')),
                ('bln_furrow_type', models.BooleanField(verbose_name='It is an open-ended furrow.')),
                ('discharge', models.DecimalField(decimal_places=4, max_digits=20, null=True, verbose_name='Unit Discharge (lps)')),
                ('area_slope', models.DecimalField(decimal_places=4, max_digits=20, null=True, verbose_name='Slope')),
                ('p_adjusted', models.DecimalField(decimal_places=4, max_digits=20, null=True, verbose_name='P adjusted (m)')),
                ('farm_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.Farm')),
                ('fieldunit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.FieldUnit')),
            ],
            options={
                'verbose_name_plural': 'Irrigation System: Furrow',
            },
        ),
        migrations.CreateModel(
            name='DripPara',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, null=True, verbose_name='System Name')),
                ('bln_single_lateral', models.BooleanField(verbose_name='Is a Single Straight Lateral type.')),
                ('emitters_per_plant', models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='No. of Emitters per Plant')),
                ('emitter_spacing', models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Emitter Spacing (m)')),
                ('optimum_emitter_spacing', models.DecimalField(decimal_places=2, help_text='This is only computed for non-single straight lateral system.', max_digits=5, null=True, verbose_name='Optimum Emitter Spacing (m)')),
                ('plant_spacing', models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Plant spacing (m)')),
                ('row_spacing', models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Row spacing (m)')),
                ('wetted_width', models.DecimalField(decimal_places=2, help_text='Leave blank if wetted portion is circular.', max_digits=5, null=True, verbose_name='Wetted width (m)')),
                ('wetted_dia', models.DecimalField(decimal_places=2, help_text='Leave blank if wetted width is filled out.', max_digits=5, null=True, verbose_name='Wetted diameter (m)')),
                ('EU', models.DecimalField(decimal_places=2, max_digits=3, null=True, verbose_name='Design Emission Uniformity')),
                ('irrigation_interval', models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Irrigation Interval (days)')),
                ('farm_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.Farm')),
                ('fieldunit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.FieldUnit', verbose_name='Field unit')),
            ],
            options={
                'verbose_name_plural': 'Irrigation System: Drip',
            },
        ),
        migrations.CreateModel(
            name='BorderPara',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('border_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='System Name')),
                ('discharge', models.DecimalField(decimal_places=4, max_digits=20, null=True, verbose_name='Unit Discharge (lps)')),
                ('border_width', models.DecimalField(decimal_places=4, max_digits=20, null=True, verbose_name='Border Width (m)')),
                ('num_of_border_strips', models.DecimalField(decimal_places=4, max_digits=20, null=True, verbose_name='Number of Borders')),
                ('mannings_coeff', models.DecimalField(decimal_places=4, max_digits=20, null=True, verbose_name="Manning's coefficient")),
                ('area_slope', models.DecimalField(decimal_places=4, max_digits=20, null=True, verbose_name='Slope')),
                ('ea', models.DecimalField(choices=[(50, '50'), (55, '55'), (60, '60'), (70, '70'), (75, '75'), (80, '80'), (85, '85'), (90, '90'), (95, '95')], decimal_places=2, max_digits=5, null=True, verbose_name='Application Efficiency (%)')),
                ('flow_rate_per_strip', models.DecimalField(decimal_places=4, max_digits=20, null=True, verbose_name='Flow rate per border strip (lps)')),
                ('total_flow_rate', models.DecimalField(decimal_places=4, max_digits=20, null=True, verbose_name='Total flow rate (lps)')),
                ('farm_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.Farm')),
                ('fieldunit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.FieldUnit')),
            ],
            options={
                'verbose_name_plural': 'Irrigation System: Border',
            },
        ),
        migrations.CreateModel(
            name='BasinPara',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basin_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='System Name')),
                ('discharge', models.DecimalField(decimal_places=4, max_digits=20, null=True, verbose_name='Unit Discharge (lps)')),
                ('basin_length', models.DecimalField(decimal_places=4, max_digits=20, null=True, verbose_name='Basin Length (m)')),
                ('ea', models.DecimalField(choices=[(50, '50'), (55, '55'), (60, '60'), (70, '70'), (75, '75'), (80, '80'), (85, '85'), (90, '90'), (95, '95')], decimal_places=2, max_digits=5, null=True, verbose_name='Application Efficiency (%)')),
                ('eff_adv_ratio', models.DecimalField(decimal_places=2, max_digits=3, null=True, verbose_name='R')),
                ('farm_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.Farm')),
                ('fieldunit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.FieldUnit')),
            ],
            options={
                'verbose_name_plural': 'Irrigation System: Basin',
            },
        ),
    ]
