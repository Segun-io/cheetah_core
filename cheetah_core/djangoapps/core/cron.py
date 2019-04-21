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
        return
    
    data_items = data['result'][data_name]

    for data_item in data_items:
        try:
            obj.objects.get(pk=data_item['id'])
            continue
        except obj.DoesNotExist:
            new_instance = obj()
            new_instance.id = data_item['id']
            new_instance.name = data_item['name']
            new_instance.localized_name = data_item['localized_name']
            new_instance.save()


def populate_heroes():
    populate_instance(Hero, API_HEROES_URL, 'heroes')

def populate_items():
    populate_instance(Item, API_ITEMS_URL, 'items')
