# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0028_auto_20161218_1459'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='google_id',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
