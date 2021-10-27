# Generated by Django 3.0.8 on 2021-02-15 07:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('waissapp', '0085_auto_20210215_1451'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='waissystems',
            options={'ordering': ('name',), 'verbose_name_plural': 'WAISSystems'},
        ),
        migrations.RenameField(
            model_name='waissystems',
            old_name='system_name',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='waissystems',
            name='farm',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.Farm', verbose_name='Farm'),
        ),
    ]