# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='category',
        ),
        migrations.RemoveField(
            model_name='topicpages',
            name='page',
        ),
        migrations.RemoveField(
            model_name='topicpages',
            name='topic',
        ),
        migrations.DeleteModel(
            name='Topic',
        ),
        migrations.DeleteModel(
            name='TopicCategory',
        ),
        migrations.DeleteModel(
            name='TopicPages',
        ),
    ]
