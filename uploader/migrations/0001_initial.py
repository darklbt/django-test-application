# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExifProperties',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('camera_vendor', models.CharField(max_length=120, null=True)),
                ('camera_model', models.CharField(max_length=120, null=True)),
                ('creation_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'')),
                ('thumbnail', models.ImageField(upload_to=b'')),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('exif', models.OneToOneField(to='uploader.ExifProperties')),
            ],
        ),
    ]
