# Generated by Django 3.0.8 on 2020-09-18 05:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('waissapp', '0048_receivedmsgs_receiver_sender_sentmsgs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentmsgs',
            name='sender_number',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='waissapp.Sender', verbose_name='Sender'),
        ),
    ]
