# Generated by Django 3.0.3 on 2020-04-29 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapps', '0002_auto_20200430_0537'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resume', models.FileField(blank=True, upload_to='photos/%Y/%m/%d/')),
            ],
        ),
        migrations.AddField(
            model_name='siteconfiguration',
            name='resume',
            field=models.FileField(blank=True, upload_to='photos/%Y/%m/%d/'),
        ),
    ]
