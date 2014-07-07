# -*- coding: utf-8 -*-
from datetime import datetime

from django.core.cache import cache
from django.db import models

from easy_thumbnails.files import get_thumbnailer

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


class TimeFrame(models.Model):
    """
    Time frame for the Food.
    Food can only be available in the specific time frame.
    """
    name = models.CharField(u'名字', max_length=128)
    shop = models.ForeignKey(Shop)
    foods = models.ManyToManyField(verbose_name=u'菜品', to=Food)
    start_time = models.TimeField(u'开始时间')
    end_time = models.TimeField(u'结束时间')
    is_active = models.BooleanField(u'启用', default=True)

    def __unicode__(self):
        return self.name

    @property
    def available_foods(self):
        """
        Get all available foods for the time frame.
        """
        cache_key = 'time_frame_foods_{}'.format(self.id)
        if not cache.get(cache_key):
            foods = []
            for food in self.foods.filter(is_active=True):
                foods.append({
                    'id': food.id,
                    'name': food.name,
                    'price': food.price,
                    'description': food.description,
                    'ingredients': food.ingredients,
                    'image': get_thumbnailer(food.image).get_thumbnail({'size': (256, 256)}).url  # noqa
                })
            cache.set(cache_key, foods, 300)  # cache for 5 mins
        return cache.get(cache_key)

    @property
    def time(self):
        return u'{}-{}'.format(self.start_time.strftime('%H:%M'),
                                self.end_time.strftime('%H:%M'))

    @property
    def is_available(self):
        now = datetime.now()
        return now.time() >= self.start_time and now.time() < self.end_time
