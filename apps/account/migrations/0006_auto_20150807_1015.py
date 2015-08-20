# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20150807_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='city',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='account',
            name='country',
            field=models.CharField(max_length=255),
        ),
    ]
