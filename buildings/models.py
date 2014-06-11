# -*- coding: utf-8 -*-
from django.db import models

from shops.models import Shop


class Building(models.Model):
    """
    Office building model.

    Building A:
        floor 3
        floor 2
        floor 1

    Building B:
        Zone-1
            floor 3
            floor 2
            floor 1
        Zone-2
            floor 3
            floor 2
            floor 1
    """
    name = models.CharField(max_length=128)
    shop = models.ForeignKey(Shop)
    is_multiple = models.BooleanField(default=True)
    # floors field only be available when building is single.
    floors = models.SmallIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


class Zone(models.Model):
    """
    Office building zone model.
    Each office building can have more than one zone.
    """
    building = models.ForeignKey(Building)
    name = models.CharField(max_length=128)
    floors = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


class Room(models.Model):
    """
    Office building room model.
    One room always mean a company.
    """
    building = models.ForeignKey(Building)
    zone = models.ForeignKey(Zone, blank=True, null=True)
    floor = models.SmallIntegerField()
    number = models.CharField(max_length=16)
    company_name = models.CharField(max_length=128, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.number
