# Generated by Django 3.0.8 on 2021-02-17 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waissapp', '0091_auto_20210217_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='crop',
            name='root_growth_model',
            field=models.CharField(blank=True, choices=[('rgm1', 'Borg-Grimes Model'), ('rgm2', 'User-Defined'), ('rgm3', 'Inverse Kc')], max_length=30, null=True, verbose_name='Root Growth Model'),
        ),
    ]