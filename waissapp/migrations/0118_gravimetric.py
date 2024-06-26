# Generated by Django 3.0.8 on 2021-03-16 01:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('waissapp', '0117_auto_20210312_1327'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gravimetric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(null=True, verbose_name='Date & Time Measured')),
                ('mc_data', models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='MCv (%)')),
                ('note', models.CharField(blank=True, max_length=100, null=True, verbose_name='Remarks')),
                ('fieldunit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.Sensor')),
            ],
        ),
    ]
