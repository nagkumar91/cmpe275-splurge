# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20151130_1027'),
    ]

    operations = [
        migrations.CreateModel(
            name='GiftCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('amount', models.IntegerField(default=0)),
                ('expired', models.BooleanField(default=False)),
                ('claimed', models.BooleanField(default=False)),
                ('expiry_timestamp', models.DateTimeField(null=True, blank=True)),
                ('given_by', models.ForeignKey(related_name='gift_cards', to=settings.AUTH_USER_MODEL)),
                ('to', models.ForeignKey(related_name='gift_cards', to='core.Employee')),
            ],
            options={
                'verbose_name': 'Gift Card',
                'verbose_name_plural': 'Gift Cards',
            },
        ),
    ]
