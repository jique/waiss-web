# Generated by Django 3.0.8 on 2020-11-06 08:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('waissapp', '0060_auto_20201104_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='farm',
            name='sensors',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.SensorNumber'),
        ),
    ]
