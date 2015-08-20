# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_emailchange'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='education_level',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='account',
            name='university',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='city',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='country',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
