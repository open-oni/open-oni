# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_copyright_lccndatecopyright'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='essay',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='essay',
            name='titles',
        ),
        migrations.AddField(
            model_name='title',
            name='essay',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Essay',
        ),
    ]
