# Generated by Django 3.1.3 on 2021-02-15 21:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20210215_1833'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postlike',
            name='likes',
        ),
    ]