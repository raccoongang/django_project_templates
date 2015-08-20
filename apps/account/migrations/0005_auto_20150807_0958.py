# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20150807_0624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='city',
            field=models.CharField(default=b'?', max_length=255),
        ),
        migrations.AlterField(
            model_name='account',
            name='country',
            field=models.CharField(default=b'?', max_length=255),
        ),
    ]
