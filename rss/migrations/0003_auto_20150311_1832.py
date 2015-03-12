# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('rss', '0002_auto_20150311_0020'),
    ]

    operations = [
        migrations.CreateModel(
            name='WordType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('number', models.IntegerField(default=0)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('word', models.ForeignKey(to='rss.Word')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='wordtype',
            unique_together=set([('content_type', 'object_id', 'word')]),
        ),
        migrations.RenameField(
            model_name='word',
            old_name='count',
            new_name='number',
        ),
    ]
