# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20151201_2112'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='balance',
            field=models.IntegerField(default=0),
        ),
    ]
