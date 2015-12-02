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
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('unique_code', models.CharField(max_length=25, serialize=False, primary_key=True)),
                ('amount', models.IntegerField(default=0)),
                ('email_notification', models.BooleanField(default=False)),
                ('expiry_reminder', models.BooleanField(default=False)),
                ('expired', models.BooleanField(default=False)),
                ('claimed', models.BooleanField(default=False)),
                ('expiry_timestamp', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Gift Card',
                'verbose_name_plural': 'Gift Cards',
            },
        ),
        migrations.CreateModel(
            name='GiftCardCategory',
            fields=[
                ('name', models.CharField(max_length=25, unique=True, serialize=False, primary_key=True)),
            ],
            options={
                'verbose_name': 'Gift Card Category',
                'verbose_name_plural': 'Gift Card Categories',
            },
        ),
        migrations.CreateModel(
            name='GiftCardRedeemableSite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('site_name', models.CharField(unique=True, max_length=1024)),
            ],
        ),
        migrations.AddField(
            model_name='giftcardcategory',
            name='sites',
            field=models.ManyToManyField(related_name='categories', to='core.GiftCardRedeemableSite'),
        ),
        migrations.AddField(
            model_name='giftcard',
            name='category',
            field=models.ForeignKey(related_name='gift_cards', to='core.GiftCardCategory'),
        ),
        migrations.AddField(
            model_name='giftcard',
            name='given_by',
            field=models.ForeignKey(related_name='gift_cards', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='giftcard',
            name='to',
            field=models.ForeignKey(related_name='gift_cards', to='core.Employee'),
        ),
    ]
