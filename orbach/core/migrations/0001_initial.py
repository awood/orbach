# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import orbach.core.util
import orbach.core.storage
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cover',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'ob_covers',
            },
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=175)),
                ('description', models.TextField(max_length=300)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(to='core.Gallery')),
            ],
            options={
                'verbose_name_plural': 'galleries',
                'db_table': 'ob_galleries',
            },
        ),
        migrations.CreateModel(
            name='ImageFile',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('file', models.ImageField(upload_to=orbach.core.util.image_dir, max_length=150, storage=orbach.core.storage.HashDistributedStorage, height_field='height', width_field='width')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ob_image_files',
            },
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('caption', models.TextField(max_length=250)),
                ('title', models.TextField(max_length=50)),
                ('gallery', models.ForeignKey(to='core.Gallery')),
                ('image', models.ForeignKey(to='core.ImageFile')),
            ],
            options={
                'db_table': 'ob_pictures',
            },
        ),
        migrations.AddField(
            model_name='cover',
            name='gallery',
            field=models.ForeignKey(to='core.Gallery'),
        ),
        migrations.AddField(
            model_name='cover',
            name='picture',
            field=models.ForeignKey(to='core.Picture'),
        ),
        migrations.AlterUniqueTogether(
            name='picture',
            unique_together=set([('id', 'gallery')]),
        ),
        migrations.AlterUniqueTogether(
            name='cover',
            unique_together=set([('gallery', 'picture')]),
        ),
        migrations.AlterModelOptions(
            name='gallery',
            options={'permissions': (('view_task', 'View task'),), 'verbose_name_plural': 'galleries'},
        ),
        migrations.AlterModelOptions(
            name='imagefile',
            options={'permissions': (('view_task', 'View task'),)},
        ),
        migrations.AlterModelOptions(
            name='picture',
            options={'permissions': (('view_task', 'View task'),)},
        ),
        migrations.AddField(
            model_name='imagefile',
            name='height',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='imagefile',
            name='width',
            field=models.IntegerField(default=0),
        ),
    ]
