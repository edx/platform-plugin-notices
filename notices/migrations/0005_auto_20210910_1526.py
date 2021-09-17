# Generated by Django 2.2.24 on 2021-09-10 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notices', '0004_auto_20210908_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalnotice',
            name='head_content',
            field=models.TextField(default='', help_text='HTML content to be included in the <head> block. Should contain all javascript / styles. Shared for all translated templates'),
        ),
        migrations.AddField(
            model_name='notice',
            name='head_content',
            field=models.TextField(default='', help_text='HTML content to be included in the <head> block. Should contain all javascript / styles. Shared for all translated templates'),
        ),
        migrations.AlterField(
            model_name='historicaltranslatednoticecontent',
            name='html_content',
            field=models.TextField(help_text="HTML content to be included in a notice view's <body> block."),
        ),
        migrations.AlterField(
            model_name='historicaltranslatednoticecontent',
            name='language_code',
            field=models.CharField(help_text='The 2 character shortcode language (en, es, etc.)', max_length=10),
        ),
        migrations.AlterField(
            model_name='translatednoticecontent',
            name='html_content',
            field=models.TextField(help_text="HTML content to be included in a notice view's <body> block."),
        ),
        migrations.AlterField(
            model_name='translatednoticecontent',
            name='language_code',
            field=models.CharField(help_text='The 2 character shortcode language (en, es, etc.)', max_length=10),
        ),
    ]