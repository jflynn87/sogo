# Generated by Django 2.0.4 on 2018-11-05 05:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sogo_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='results',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='sogo_app.User'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='activities',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='results',
            unique_together={('date', 'activity', 'user')},
        ),
    ]
