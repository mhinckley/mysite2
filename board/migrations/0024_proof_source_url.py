# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0023_proof'),
    ]

    operations = [
        migrations.AddField(
            model_name='proof',
            name='source_url',
            field=models.URLField(max_length=300, null=True, blank=True),
        ),
    ]
