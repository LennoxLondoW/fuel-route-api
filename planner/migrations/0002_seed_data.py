"""
Data migration: seed the City and FuelStation tables from html/cities.js and html/stations.js,
so a fresh "manage.py migrate" gives a working API with no extra steps.

To reload the data later (e.g. new prices), use:  python manage.py load_data
"""

from django.db import migrations


def seed(apps, schema_editor):
    """Fill both tables (uses the historical models, as migrations must)."""
    from planner.data_loader import load

    City = apps.get_model("planner", "City")
    FuelStation = apps.get_model("planner", "FuelStation")
    cities, stations = load(City, FuelStation)
    print(f"\n  Seeded {cities} cities and {stations} fuel stations.", end="")


def unseed(apps, schema_editor):
    """Reverse: empty both tables."""
    apps.get_model("planner", "City").objects.all().delete()
    apps.get_model("planner", "FuelStation").objects.all().delete()


class Migration(migrations.Migration):
    """Seeds cities and fuel stations."""

    dependencies = [("planner", "0001_initial")]

    operations = [migrations.RunPython(seed, unseed)]
