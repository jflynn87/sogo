# Generated by Django 2.0.4 on 2018-11-16 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sogo_app', '0012_auto_20181115_2315'),
    ]

    operations = [
        migrations.RenameField(
            model_name='results',
            old_name='duration',
            new_name='result',
        ),
    ]
