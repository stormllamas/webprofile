# Generated by Django 2.2.3 on 2019-09-13 05:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendees', '0021_auto_20190913_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitylog',
            name='attendee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity', to='attendees.Attendee'),
        ),
        migrations.AlterField(
            model_name='activitylog',
            name='time_log',
            field=models.DateTimeField(null=True, verbose_name='time_logs'),
        ),
    ]
