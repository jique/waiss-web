# Generated by Django 3.0.8 on 2021-07-29 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waissapp', '0153_auto_20210729_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='border',
            name='bln_irrigation',
            field=models.CharField(blank=True, choices=[('True', 'Yes, I do!'), ('False', 'No, I dont.')], max_length=6, null='True', verbose_name='Do you have an irrigation system?'),
        ),
        migrations.AlterField(
            model_name='border',
            name='select_irrigation',
            field=models.CharField(blank=True, choices=[('basin', 'basin'), ('border', 'border'), ('furrow', 'furrow'), ('sprinkler', 'sprinkler'), ('drip', 'drip')], max_length=30, null=True, verbose_name='Select Irrigation System Type'),
        ),
        migrations.AlterField(
            model_name='drip',
            name='bln_irrigation',
            field=models.CharField(blank=True, choices=[('True', 'Yes, I do!'), ('False', 'No, I dont.')], max_length=6, null='True', verbose_name='Do you have an irrigation system?'),
        ),
        migrations.AlterField(
            model_name='drip',
            name='select_irrigation',
            field=models.CharField(blank=True, choices=[('basin', 'basin'), ('border', 'border'), ('furrow', 'furrow'), ('sprinkler', 'sprinkler'), ('drip', 'drip')], max_length=30, null=True, verbose_name='Select Irrigation System Type'),
        ),
        migrations.AlterField(
            model_name='furrow',
            name='bln_irrigation',
            field=models.CharField(blank=True, choices=[('True', 'Yes, I do!'), ('False', 'No, I dont.')], max_length=6, null=True, verbose_name='Do you have an irrigation system?'),
        ),
        migrations.AlterField(
            model_name='furrow',
            name='select_irrigation',
            field=models.CharField(blank=True, choices=[('basin', 'basin'), ('border', 'border'), ('furrow', 'furrow'), ('sprinkler', 'sprinkler'), ('drip', 'drip')], max_length=30, null=True, verbose_name='Select Irrigation System Type'),
        ),
        migrations.AlterField(
            model_name='sprinkler',
            name='bln_irrigation',
            field=models.CharField(blank=True, choices=[('True', 'Yes, I do!'), ('False', 'No, I dont.')], max_length=6, null='True', verbose_name='Do you have an irrigation system?'),
        ),
        migrations.AlterField(
            model_name='sprinkler',
            name='select_irrigation',
            field=models.CharField(blank=True, choices=[('basin', 'basin'), ('border', 'border'), ('furrow', 'furrow'), ('sprinkler', 'sprinkler'), ('drip', 'drip')], max_length=30, null=True, verbose_name='Select Irrigation System Type'),
        ),
    ]
