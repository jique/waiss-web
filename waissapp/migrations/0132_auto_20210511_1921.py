# Generated by Django 3.0.8 on 2021-05-11 11:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('waissapp', '0131_auto_20210511_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drip',
            name='author',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='drip',
            name='bln_ii',
            field=models.BooleanField(null=True, verbose_name='Has preferred irrigation interval'),
        ),
        migrations.AlterField(
            model_name='drip',
            name='bln_single_lateral',
            field=models.BooleanField(null=True, verbose_name='Single Straight Lateral'),
        ),
        migrations.AlterField(
            model_name='drip',
            name='discharge',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Emitter Discharge (l/day)'),
        ),
        migrations.AlterField(
            model_name='drip',
            name='emitter_spacing',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Emitter Spacing (m)'),
        ),
        migrations.AlterField(
            model_name='drip',
            name='emitters_per_plant',
            field=models.DecimalField(decimal_places=0, max_digits=5, null=True, verbose_name='No. of Emitters per Plant'),
        ),
        migrations.AlterField(
            model_name='drip',
            name='plant_spacing',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Plant spacing (m)'),
        ),
        migrations.AlterField(
            model_name='drip',
            name='row_spacing',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Row spacing (m)'),
        ),
        migrations.AlterField(
            model_name='drip',
            name='wetted_dia',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Wetted diameter (m)'),
        ),
        migrations.AlterField(
            model_name='gravimetric',
            name='timestamp',
            field=models.DateTimeField(help_text='Format: mm/dd/yyyy hh:mm (should be an exact counterpart on MCv datapoints)', null=True, verbose_name='Date & Time'),
        ),
        migrations.AlterField(
            model_name='moisturecontent',
            name='timestamp',
            field=models.DateTimeField(help_text='Format: mm/dd/yyyy hh:mm', null=True, verbose_name='Date & Time Measured'),
        ),
        migrations.AlterField(
            model_name='percentshaded',
            name='area_shaded',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Area Shaded (%)'),
        ),
        migrations.AlterField(
            model_name='percentshaded',
            name='crop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.Crop', verbose_name='Crop'),
        ),
        migrations.AlterField(
            model_name='percentshaded',
            name='date',
            field=models.DateField(null=True, verbose_name='Date'),
        ),
    ]
