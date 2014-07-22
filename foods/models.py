# -*- coding: utf-8 -*-
import json
from datetime import datetime

from django.core.cache import cache
from django.db import models

from easy_thumbnails.files import get_thumbnailer

from accounts.models import Address
from shops.models import Shop
from foods.constants import DELICIOUS, SOSO, BAD


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
    description = models.TextField(blank=True)
    ingredients = models.TextField(blank=True)
    image = models.ImageField(upload_to='foods')
    tips = models.TextField(blank=True)
    is_primary = models.BooleanField(default=True)
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
    RATING_CHOICES = (
        (DELICIOUS, u'好吃'),
        (SOSO, u'一般'),
        (BAD, u'不好吃'),
    )
    food = models.ForeignKey(Food)
    address = models.ForeignKey(Address, blank=True, null=True)
    rating = models.CharField(max_length=16, choices=RATING_CHOICES,
                              db_index=True, default=DELICIOUS)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def rating_class(self):
        if self.rating == DELICIOUS:
            return 'glyphicon-thumbs-up'
        elif self.rating == BAD:
            return 'glyphicon-thumbs-down'
        return ''


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
    sections = models.TextField(u'下单时段')
    is_active = models.BooleanField(u'启用', default=True)

    def __unicode__(self):
        return self.name

    @property
    def sections_list(self):
        try:
            sections = []
            for section in json.loads(self.sections):
                sections.append({
                    'label': section['label'],
                    'time': datetime.strptime(section['time'], '%H:%M:%S').time()
                })
            return sections
        except:
            return []

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
                    'is_primary': food.is_primary,
                    'name': food.name,
                    'price': food.price,
                    'comment_count': food.foodcomment_set.count(),
                    'delicious_comment_count': food.foodcomment_set.filter(rating=DELICIOUS).count(),
                    'soso_comment_count': food.foodcomment_set.filter(rating=SOSO).count(),
                    'bad_comment_count': food.foodcomment_set.filter(rating=BAD).count(),
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
