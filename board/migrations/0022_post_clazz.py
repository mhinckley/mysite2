# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0021_auto_20161031_1305'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='clazz',
            field=models.CharField(default=b'Influence', max_length=50),
        ),
    ]
