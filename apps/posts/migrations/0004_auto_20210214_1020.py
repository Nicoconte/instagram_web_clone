# Generated by Django 3.1.3 on 2021-02-14 13:20

import apps.posts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20210214_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postimage',
            name='file',
            field=models.ImageField(default='not-image.png', upload_to=apps.posts.models.path),
        ),
    ]
