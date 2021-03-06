# Generated by Django 2.2.24 on 2021-10-07 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notices', '0005_auto_20210910_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaltranslatednoticecontent',
            name='language_code',
            field=models.CharField(help_text='The language code (e.g. en, es-419). Must be a released language in DarkLang if DarkLang is enabled.', max_length=10),
        ),
        migrations.AlterField(
            model_name='translatednoticecontent',
            name='language_code',
            field=models.CharField(help_text='The language code (e.g. en, es-419). Must be a released language in DarkLang if DarkLang is enabled.', max_length=10),
        ),
    ]
