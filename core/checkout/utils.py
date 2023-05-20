import json

from django.contrib.staticfiles import finders
from django.core.files import File


def getCities():
    result = finders.find("data/cities.json")
    with open(result, "r", encoding='utf-8') as f:
        citiesFile = File(f)
        cities: list = [item['city'] for item in json.loads(citiesFile.read())]
    return cities