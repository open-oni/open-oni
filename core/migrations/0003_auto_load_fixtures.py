# -*- coding: utf-8 -*-

from django.core import serializers
from django.core.management import call_command
from django.db import migrations, models
import os

fixture_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../fixtures'))

def load_fixture(fixture_filename):
    fixture_file = os.path.join(fixture_dir, fixture_filename)

    fixture = open(fixture_file, 'rb')
    objects = serializers.deserialize('json', fixture, ignorenonexistent=True)
    for obj in objects:
        obj.save()
    fixture.close()

class Migration(migrations.Migration):
    def load_data(apps, schema_editor):
        load_fixture("awardees.json")
        load_fixture("countries.json")
        load_fixture("material_types.json")
        load_fixture("languages.json")
        load_fixture("institutions.json")
        load_fixture("ethnicities.json")
        load_fixture("labor_presses.json")
        load_fixture("countries.json")

    dependencies = [
        ("core", "0002_auto_20160713_1509"),
    ]

    operations = [
      migrations.RunPython(load_data)
    ]
