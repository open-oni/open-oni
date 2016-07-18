# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_load_fixtures'),
    ]

    operations = [
        migrations.CreateModel(
            name='Copyright',
            fields=[
                ('uri', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('label', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='LccnDateCopyright',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lccn', models.CharField(max_length=25)),
                ('start_date', models.IntegerField()),
                ('end_date', models.IntegerField()),
                ('uri', models.ForeignKey(related_name='lccn_date_copyright', to='core.Copyright')),
            ],
        ),
    ]
