from django.db import models
from core.models import ValveDataAbstract

class Item(ValveDataAbstract):

    CATEGORY_BUYABLE_ITEM = 'A'
    CATEGORY_UNAVAILABLE_ITEM = 'B'

    CATEGORY_CODES = (
        (CATEGORY_BUYABLE_ITEM, 'Buyable'),
        (CATEGORY_UNAVAILABLE_ITEM, 'Unavailable'),
    )

    is_recipe = models.BooleanField('Is item recipe?', default=False)
    cost = models.PositiveIntegerField('Item cost', default=0)
    category = models.CharField(
        'Item category', max_length=1, choices=CATEGORY_CODES, default=CATEGORY_BUYABLE_ITEM)
