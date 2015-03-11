# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rss', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='url',
            field=models.URLField(unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='feed',
            name='url',
            field=models.URLField(unique=True),
            preserve_default=True,
        ),
    ]
