# Generated by Django 2.0.4 on 2018-11-30 00:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sogo_app', '0016_auto_20181121_1842'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activities',
            name='beginner_target',
        ),
        migrations.RemoveField(
            model_name='activities',
            name='expert_target',
        ),
    ]