# Generated by Django 3.0.8 on 2021-01-28 06:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('waissapp', '0079_receivedmsgs_marker'),
    ]

    operations = [
        migrations.AddField(
            model_name='receivedmsgs',
            name='fieldunit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.FieldUnit'),
        ),
        migrations.AddField(
            model_name='sentmsgs',
            name='fieldunit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.FieldUnit'),
        ),
        migrations.AlterField(
            model_name='receivedmsgs',
            name='marker',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='receivedmsgs',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date/Time Sent'),
        ),
        migrations.AlterField(
            model_name='sentmsgs',
            name='marker',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='sentmsgs',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date/Time Sent'),
        ),
    ]