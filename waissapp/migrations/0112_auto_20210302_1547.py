# Generated by Django 3.0.8 on 2021-03-02 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waissapp', '0111_auto_20210301_1532'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='calibrationconstant',
            name='fieldunit',
        ),
        migrations.RemoveField(
            model_name='irrigationparameters',
            name='border_length',
        ),
        migrations.RemoveField(
            model_name='irrigationparameters',
            name='border_strips',
        ),
        migrations.RemoveField(
            model_name='irrigationparameters',
            name='flow_rate_per_strip',
        ),
        migrations.RemoveField(
            model_name='irrigationparameters',
            name='total_flow_rate',
        ),
        migrations.RemoveField(
            model_name='irrigationparameters',
            name='width',
        ),
        migrations.AlterField(
            model_name='calibrationconstant',
            name='calib_equation',
            field=models.CharField(choices=[('linear', 'Linear'), ('quadratic', 'Quadratic'), ('exponential', 'Exponential'), ('logarithmic', 'Logarithmic'), ('symmetrical sigmoidal', 'Symmetrical Sigmoidal'), ('asymmetrical sigmoidal', 'Asymmetrical Sigmoidal')], default='linear', max_length=30, null=True, verbose_name='Equation Form'),
        ),
        migrations.AlterField(
            model_name='calibrationconstant',
            name='name',
            field=models.CharField(max_length=25, null=True, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='crop',
            name='crop',
            field=models.CharField(max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='crop',
            name='date_transplanted',
            field=models.DateField(null=True, verbose_name='Date Transplanted'),
        ),
        migrations.AlterField(
            model_name='crop',
            name='growingperiod',
            field=models.IntegerField(null=True, verbose_name='Growing Period, days'),
        ),
        migrations.AlterField(
            model_name='crop',
            name='mad',
            field=models.DecimalField(decimal_places=2, max_digits=3, null=True, verbose_name='Management Allowable Deficit'),
        ),
        migrations.AlterField(
            model_name='crop',
            name='root_growth_model',
            field=models.CharField(choices=[('Borg-Grimes Model', 'Borg-Grimes Model'), ('User-Defined', 'User-Definerd'), ('Inverse Kc', 'Inverse Kc')], max_length=30, null=True, verbose_name='Root Growth Model'),
        ),
        migrations.AlterField(
            model_name='irrigationparameters',
            name='irrigation_system_type',
            field=models.CharField(choices=[('basin', 'basin'), ('border', 'border'), ('furrow', 'furrow'), ('sprinkler', 'sprinkler'), ('drip', 'drip')], max_length=30, null=True, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='irrigationparameters',
            name='name',
            field=models.CharField(max_length=30, null=True, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='first_name',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='last_name',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='number',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='soil',
            name='fc',
            field=models.DecimalField(decimal_places=2, max_digits=4, null=True, verbose_name='Field Capacity (% vol)'),
        ),
        migrations.AlterField(
            model_name='soil',
            name='pwp',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Permanent Wilting Point (% vol)'),
        ),
        migrations.AlterField(
            model_name='soil',
            name='soiltype',
            field=models.CharField(max_length=25, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='soil',
            name='source',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Data Source'),
        ),
    ]
