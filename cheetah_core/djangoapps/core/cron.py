import requests

from django.conf import settings

from heroes.models import Hero
from items.models import Item

STEAM_API_KEY = settings.STEAM_API_KEY

API_HEROES_URL = 'http://api.steampowered.com/IEconDOTA2_570/GetHeroes/v1?key={}&language=en_us'.format(
    STEAM_API_KEY)

API_ITEMS_URL = 'http://api.steampowered.com/IEconDOTA2_570/GetGameItems/v1?key={}&language=en_us'.format(
    STEAM_API_KEY)

def populate_instance(obj, api, data_name):
    objs_count = obj.objects.count()
    request = requests.get(api)
    data = request.json()
    
    if objs_count == data['result'].get('count', -1):
        return False
    
    return data['result'][data_name]




def populate_heroes():
    heroes = populate_instance(Hero, API_HEROES_URL, 'heroes')

    for hero in heroes:
        try:
            Hero.objects.get(pk=hero['id'])
            continue
        except Hero.DoesNotExist:
            new_instance = Hero()
            new_instance.id = hero['id']
            new_instance.name = hero['name']
            new_instance.localized_name = hero['localized_name']
            new_instance.save()


def populate_items():
    items = populate_instance(Item, API_ITEMS_URL, 'items')

    for item in items:
        try:
            Item.objects.get(pk=item['id'])
            continue
        except Item.DoesNotExist:
            new_instance = Item()
            new_instance.id = item['id']
            new_instance.name = item['name']
            new_instance.localized_name = item['localized_name']
            new_instance.is_recipe = item['recipe']
            new_instance.cost = item['cost']
            new_instance.save()
