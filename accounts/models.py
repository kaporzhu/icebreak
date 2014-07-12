# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils.crypto import get_random_string

from buildings.models import Building, Zone, Room
from shops.models import Shop


class Staff(models.Model):
    """
    Staff model
    """
    user = models.OneToOneField(User)
    phone = models.CharField(u'手机号', max_length=16, blank=True, null=True)
    is_deliveryman = models.BooleanField(u'配送员')
    is_shop_manager = models.BooleanField(u'店长')
    shop = models.ForeignKey(Shop)
    api_key = models.CharField(max_length=16, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def role_name(self):
        if self.is_shop_manager:
            return u'店长'
        elif self.is_deliveryman:
            return u'配送员'
        else:
            return ''


class Address(models.Model):
    """
    User address
    """
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=16)
    name = models.CharField(max_length=128)
    building = models.ForeignKey(Building)
    zone = models.ForeignKey(Zone, blank=True, null=True)
    room = models.ForeignKey(Room)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        address = self.building.name
        if self.building.is_multiple:
            address += self.zone.name
        address += self.room.number
        return address


def create_api_key(sender, instance, **kwargs):
    """
    A signal for hooking up automatic ``ApiKey`` creation.
    """
    if kwargs.get('created') is True:
        instance.api_key = get_random_string(16)
        instance.save(using=False)


post_save.connect(create_api_key, sender=Staff)
