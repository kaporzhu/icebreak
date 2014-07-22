# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils.crypto import get_random_string

from .constants import CHEF, DELIVERYMAN, MANAGER
from buildings.models import Building, Zone, Room
from shops.models import Shop


class Staff(models.Model):
    """
    Staff model
    """
    ROLE_CHOICES = (
        (MANAGER, u'店长'),
        (DELIVERYMAN, u'配送员'),
        (CHEF, u'厨师'),
    )

    user = models.OneToOneField(User)
    phone = models.CharField(u'手机号', max_length=16)
    shop = models.ForeignKey(Shop)
    role = models.CharField(u'职务', max_length=16, choices=ROLE_CHOICES,
                            default=DELIVERYMAN)
    intro = models.TextField(u'个人简介', blank=True, null=True)
    api_key = models.CharField(max_length=16)
    avatar = models.ImageField(u'头像', upload_to='avatars')
    created_at = models.DateTimeField(auto_now_add=True)


class StaffMessage(models.Model):
    """
    Message between user and the staff
    """
    staff = models.ForeignKey(Staff)
    user = models.ForeignKey(User, blank=True, null=True)
    reply_to = models.ForeignKey('self', blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-id',)


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
