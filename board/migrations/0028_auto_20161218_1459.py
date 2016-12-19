# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0027_auto_20161218_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='person',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='source_url',
            field=models.URLField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='summary',
            field=models.TextField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='to_field',
            field=models.CharField(max_length=55),
        ),
    ]
