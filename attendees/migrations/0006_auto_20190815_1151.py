# Generated by Django 2.2.3 on 2019-08-15 03:51

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('attendees', '0005_auto_20190815_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendee',
            name='time_log',
            field=models.TextField(default=[]),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 15, 3, 51, 3, 535308, tzinfo=utc), verbose_name='timestamp'),
        ),
    ]
