# -*- coding: utf-8 -*-
from django.db import models

from accounts.models import Address
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
    sales = models.IntegerField(default=0)
    count_today = models.SmallIntegerField(default=0)
    average_rate = models.FloatField(default=0)
    rate_count = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    ingredients = models.TextField(blank=True)
    image = models.ImageField(upload_to='foods')
    tips = models.TextField(blank=True)
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


class FoodComment(models.Model):
    """
    Comment for the food
    """
    food = models.ForeignKey(Food)
    address = models.ForeignKey(Address, blank=True, null=True)
    rating = models.SmallIntegerField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
