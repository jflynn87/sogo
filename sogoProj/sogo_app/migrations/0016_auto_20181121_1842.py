# Generated by Django 2.0.4 on 2018-11-21 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sogo_app', '0015_auto_20181119_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activities',
            name='target_type',
            field=models.CharField(choices=[('T', 'Time'), ('R', 'Sets & Reps')], max_length=1),
        ),
        migrations.AlterField(
            model_name='gritactivity',
            name='challenge',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity', to='sogo_app.GritChallenge'),
        ),
    ]