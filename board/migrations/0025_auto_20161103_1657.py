# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0024_proof_source_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proof',
            name='caption',
            field=models.CharField(max_length=105, null=True, blank=True),
        ),
    ]
