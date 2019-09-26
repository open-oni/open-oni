# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_load_fixtures'),
    ]

    operations = [
        migrations.CreateModel(
            name='Copyright',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uri', models.CharField(max_length=100)),
                ('label', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='LccnDateCopyright',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lccn', models.CharField(max_length=25)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('copyright', models.ForeignKey(related_name='lccn_date_copyright', to='core.Copyright')),
            ],
        ),
    ]
