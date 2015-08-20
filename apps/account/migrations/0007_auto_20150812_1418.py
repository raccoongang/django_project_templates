# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20150807_1015'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='linkedin',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='account',
            name='odnoklassniki',
            field=models.URLField(null=True, blank=True),
        ),
    ]
