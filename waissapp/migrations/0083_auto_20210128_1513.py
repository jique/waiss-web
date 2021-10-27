# Generated by Django 3.0.8 on 2021-01-28 07:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('waissapp', '0082_auto_20210128_1455'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fieldunit',
            old_name='mobilenumber',
            new_name='fieldunit_number',
        ),
        migrations.AddField(
            model_name='receivedmsgs',
            name='fieldunit_number',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.FieldUnit'),
        ),
        migrations.AddField(
            model_name='sentmsgs',
            name='fieldunit_number',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.FieldUnit'),
        ),
    ]