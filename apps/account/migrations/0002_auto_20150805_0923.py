# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='account',
            name='facebook',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='account',
            name='my_site',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='account',
            name='vkontakte',
            field=models.URLField(null=True, blank=True),
        ),
    ]
