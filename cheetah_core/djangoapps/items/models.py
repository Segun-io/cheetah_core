from django.db import models
from core.models import ValveDataAbstract

class Item(ValveDataAbstract):
    is_recipe = models.BooleanField('Is item recipe?', default=False)
    cost = models.PositiveIntegerField('Item cost', default=0)
