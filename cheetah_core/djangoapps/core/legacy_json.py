import os
import json

from heroes.models import Hero
from items.models import Item

legacy_fixtures = {
    'heroes': 'legacy_fixtures/heroes_merge.json',
    'items': 'legacy_fixtures/items_merge.json',
    'units': 'legacy_fixtures/units.json',
    'commands': 'legacy_fixtures/commands.json',
}

def set_nicknames(obj, fixture):
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, fixture)

    with open(file_path) as json_file:
        data = json.load(json_file)
        for d in data:
            try:
                instance = obj.objects.get(pk=d['id'])
            except obj.DoesNotExist:
                continue
            if not instance.nicknames:
                instance.nicknames = ','.join(d['abb'])
                instance.save()

def set_hero_nicknames():
    set_nicknames(Hero, legacy_fixtures['heroes'])

def set_items_nicknames():
    set_nicknames(Item, legacy_fixtures['items'])

def set_items_categories():
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, legacy_fixtures['items'])

    with open(file_path) as json_file:
        data = json.load(json_file)
        for d in data:
            try:
                instance = Item.objects.get(pk=d['id'])
            except Item.DoesNotExist:
                continue
            cat = Item.CATEGORY_BUYABLE_ITEM if d['cat'] == \
                1 else Item.CATEGORY_UNAVAILABLE_ITEM
            
            instance.category = cat
            instance.save()
