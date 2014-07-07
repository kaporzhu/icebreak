# -*- coding: utf-8 -*-
from django.core.cache import cache
from django.db import models

from easy_thumbnails.files import get_thumbnailer


class Shop(models.Model):
    """
    Shop model.
    Each shop covers about 3 office buildings.
    """
    name = models.CharField(max_length=128)
    slug = models.CharField(max_length=32, unique=True, blank=True, null=True)
    address = models.CharField(max_length=256)
    phone = models.CharField(max_length=16, blank=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    is_closed = models.BooleanField(default=False)
    close_tip = models.TextField(blank=True, null=True)

    open_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    @property
    def staffs(self):
        """
        Get all staffs for the shop.
        """
        cache_key = 'shop_staffs_{}'.format(self.id)
        if not cache.get(cache_key):
            staffs = []
            for staff in self.staff_set.filter(user__is_active=True):
                if staff.avatar:
                    avatar = get_thumbnailer(staff.avatar).get_thumbnail({'size': (64, 64)}).url  # noqa
                else:
                    avatar = None
                staffs.append({
                    'role_name': staff.role_name,
                    'full_name': staff.user.get_full_name(),
                    'avatar': avatar
                })
            cache.set(cache_key, staffs, 300)  # cache for 5 mins
        return cache.get(cache_key)

    @property
    def time_frames(self):
        """
        Get all time frames for the shop.
        """
        cache_key = 'shop_time_frames_{}'.format(self.id)
        if not cache.get(cache_key):
            time_frames = []
            for frame in self.timeframe_set.filter(is_active=True):
                time_frames.append({
                    'id': frame.id,
                    'name': frame.name,
                    'time': frame.time,
                    'is_available': frame.is_available,
                    'available_foods': frame.available_foods
                })
            cache.set(cache_key, time_frames, 30)  # cache for 30 seconds
        return cache.get(cache_key)

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
