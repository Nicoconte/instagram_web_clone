# Generated by Django 3.1.3 on 2021-02-14 12:51

import apps.posts.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20210214_0015'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=200)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
            ],
        ),
        migrations.RemoveField(
            model_name='postimage',
            name='image_path',
        ),
        migrations.AddField(
            model_name='postimage',
            name='file',
            field=models.ImageField(blank=True, default='not-image.png', null=True, upload_to=apps.posts.models.path),
        ),
        migrations.CreateModel(
            name='PostCommentAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=200)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.postcomment')),
            ],
        ),
    ]
