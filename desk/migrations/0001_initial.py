# Generated by Django 2.1.7 on 2019-04-05 11:22

import desk.model
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Title of the Column', max_length=64)),
                ('created', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Column',
                'verbose_name_plural': 'Columns',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_body', models.TextField(help_text='Comment text', max_length=500)),
                ('image', models.ImageField(blank=True, null=True, upload_to=desk.model.upload_comment_image)),
                ('is_child', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Desk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Title of the Desk', max_length=64)),
                ('description', models.TextField(help_text='Description of the Desk', max_length=500)),
            ],
            options={
                'verbose_name': 'Desk post',
                'verbose_name_plural': 'Desk posts',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Title of the task', max_length=64)),
                ('description', models.TextField(help_text='Description of the Task', max_length=500)),
                ('task_deadline', models.DateField(default=django.utils.timezone.now, help_text='Deadline of the task. format=Date(MM-DD-YYYY)')),
                ('image', models.ImageField(blank=True, null=True, upload_to=desk.model.upload_task_image)),
                ('priority', models.CharField(choices=[('Високий', 'HIGH'), ('Середній', 'MEDIUM'), ('Низький', 'LOW')], default='Середній', max_length=8)),
            ],
        ),
    ]
