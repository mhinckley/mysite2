# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0026_auto_20161103_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proof',
            name='caption',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='proof',
            name='person',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='proof',
            name='source_url',
            field=models.URLField(max_length=500, null=True, blank=True),
        ),
    ]
