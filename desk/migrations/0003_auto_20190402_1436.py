# Generated by Django 2.1.7 on 2019-04-02 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('desk', '0002_auto_20190402_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='parent_comment',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='desk.Comment'),
        ),
    ]
