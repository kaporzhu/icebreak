# -*- coding: utf-8 -*-
from django.db import models

from shops.models import Shop


class Food(models.Model):
    """
    Food model
    """
    name = models.CharField(max_length=128)
    price = models.FloatField()
    shop = models.ForeignKey(Shop)
    is_active = models.BooleanField(default=True, db_index=True)
    count = models.SmallIntegerField(default=True)
    description = models.TextField(blank=True)
    ingredients = models.TextField(blank=True)
    image = models.ImageField(upload_to='foods')
    tips = models.TextField(blank=True)
    # sales = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    @property
    def steps(self):
        return self.cookingstep_set.all().order_by('index')


class CookingStep(models.Model):
    """
    Cooking step model.
    Each food will contains several steps.
    """
    food = models.ForeignKey(Food)
    index = models.SmallIntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='cooking_steps', blank=True, null=True)
