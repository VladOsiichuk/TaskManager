# Generated by Django 2.1.7 on 2019-04-02 14:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('desk', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='current_executor',
            field=models.ForeignKey(help_text='ID of user for who task is assigned', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='task',
            name='related_column',
            field=models.ForeignKey(help_text='ID of column for which Task is related', on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='desk.Column'),
        ),
        migrations.AddField(
            model_name='desk',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='parent_comment',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='desk.Comment'),
        ),
        migrations.AddField(
            model_name='comment',
            name='related_task',
            field=models.ForeignKey(help_text='ID of task for which this one is related', on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='desk.Task'),
        ),
        migrations.AddField(
            model_name='column',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='column',
            name='related_desk',
            field=models.ForeignKey(help_text='ID of desk for which Column is related', on_delete=django.db.models.deletion.CASCADE, related_name='columns', to='desk.Desk'),
        ),
    ]
