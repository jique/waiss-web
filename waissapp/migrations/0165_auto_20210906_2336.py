# Generated by Django 3.0.8 on 2021-09-06 15:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waissapp', '0164_noirrigation_percent_covered'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='noirrigation',
            options={'verbose_name_plural': '5.f. Irrigation System: None'},
        ),
        migrations.AddField(
            model_name='noirrigation',
            name='bln_irrigation',
            field=models.CharField(choices=[('True', 'Yes, I do!'), ('False', 'No, I dont.')], max_length=6, null=True, verbose_name='Do you have an irrigation system?'),
        ),
        migrations.AlterField(
            model_name='noirrigation',
            name='percent_covered',
            field=models.IntegerField(default=50, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)], verbose_name='Percentage of the Farm Area to be Irrigated (Estimate)'),
        ),
    ]
