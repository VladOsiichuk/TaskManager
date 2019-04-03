# Generated by Django 2.1.7 on 2019-04-03 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('desk', '0007_auto_20190403_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('HIGH', 'Високий'), ('MEDIUM', 'Середній'), ('LOW', 'Низький')], default='MEDIUM', max_length=8),
        ),
    ]
