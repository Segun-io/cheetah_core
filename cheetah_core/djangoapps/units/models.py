from django.db import models

from core.models import ValveDataAbstract

class Unit(ValveDataAbstract):
    wiki_image = models.CharField('Wiki image name', max_length=128)
