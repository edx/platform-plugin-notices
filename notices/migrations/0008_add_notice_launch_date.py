# Generated by Django 2.2.24 on 2021-10-27 16:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('notices', '0007_acknowledgednotice_snooze_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalnotice',
            name='launch_date',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='All users created after this date will not be show the notice'),
        ),
        migrations.AddField(
            model_name='notice',
            name='launch_date',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='All users created after this date will not be show the notice'),
        ),
    ]
