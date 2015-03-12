# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rss', '0003_auto_20150311_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='number',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
