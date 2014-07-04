# -*- coding: utf-8 -*-
from django.core.cache import cache
from django.db import models


class Shop(models.Model):
    """
    Shop model.
    Each shop covers about 3 office buildings.
    """
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=256)
    phone = models.CharField(max_length=16, blank=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)

    open_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    def foods_count(self):
        """
        Count all the foods left today
        """
        cache_key = 'shop_foods_{}'.format(self.id)
        if not cache.get(cache_key):
            foods_count = {}
            for food in self.food_set.all():
                foods_count[food.id] = food.count_today
            cache.set(cache_key, foods_count, 300)  # cache for 5 mins
        return cache.get(cache_key)

    def update_food_count(self, food):
        """
        Update cached foods info
        """
        cache_key = 'shop_foods_{}'.format(self.id)
        foods_count = self.foods_count()
        foods_count[food.id] = food.count_today
        cache.set(cache_key, foods_count, 300)  # cache for 5 mins
