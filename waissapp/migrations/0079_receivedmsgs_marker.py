# Generated by Django 3.0.8 on 2021-01-18 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waissapp', '0078_auto_20210118_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='receivedmsgs',
            name='marker',
            field=models.BooleanField(default=False),
        ),
    ]
