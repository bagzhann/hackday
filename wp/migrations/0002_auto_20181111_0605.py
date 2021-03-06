# Generated by Django 2.1.3 on 2018-11-11 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vac',
            name='datetime',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='vac',
            name='desc',
            field=models.CharField(default='', max_length=400),
        ),
        migrations.AddField(
            model_name='vac',
            name='empler',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='vac',
            name='salary',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='vac',
            name='skills',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='vac',
            name='sphere',
            field=models.CharField(default='', max_length=200),
        ),
    ]
