# Generated by Django 3.2.8 on 2021-10-22 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notices', '0006_auto_20211007_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='acknowledgednotice',
            name='snooze_count',
            field=models.IntegerField(default=0),
        ),
    ]
