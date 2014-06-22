# -*- coding: utf-8 -*-
from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save, post_delete

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

    def _get_rooms(self, floors, rooms):
        """
        Rooms in JSON and rooms by floor in JSON
        """
        rooms_by_floor_list = []
        rooms_by_floor_dict = {i+1: [] for i in range(floors)}

        for room in rooms:
            rooms_by_floor_dict[room.floor].append({
                'id': room.id, 'number': room.number
            })
        for floor in sorted(rooms_by_floor_dict.keys(), reverse=True):
            rooms_by_floor_list.append(
                {'floor': floor, 'rooms': rooms_by_floor_dict[floor]})

        return (rooms_by_floor_dict, rooms_by_floor_list)

    def whole(self, refresh=False):
        """
        cached building info, include zone and room.
        """
        cache_key = 'building_whole_{}'.format(self.id)
        if refresh or not cache.get(cache_key):
            whole = {
                'id': self.id,
                'name': self.name,
                'is_multiple': self.is_multiple,
                'floors': self.floors
            }

            if self.is_multiple:
                whole['zones_dict'] = {}
                whole['zones_list'] = []
                for zone in self.zone_set.all():
                    zone_whole = {
                        'id': zone.id,
                        'name': zone.name,
                        'floors': zone.floors
                    }
                    whole['zones_dict'][zone.id] = zone_whole
                    whole['zones_list'].append(zone_whole)
                    rooms = zone.room_set.all()
                    rooms_by_floor_dict, rooms_by_floor_list = self._get_rooms(zone.floors, rooms)
                    zone_whole['rooms_by_floor_dict'] = rooms_by_floor_dict
                    zone_whole['rooms_by_floor_list'] = rooms_by_floor_list
            else:
                rooms = self.room_set.all()
                rooms_by_floor_dict, rooms_by_floor_list = self._get_rooms(self.floors, rooms)
                whole['rooms_by_floor_dict'] = rooms_by_floor_dict
                whole['rooms_by_floor_list'] = rooms_by_floor_list

            cache.set(cache_key, whole, 1728000)  # cache for one month

        return cache.get(cache_key)


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
    floor = models.SmallIntegerField(db_index=True)
    number = models.CharField(max_length=16)
    company_name = models.CharField(max_length=128, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.number


def update_cached_building(sender, instance, *args, **kwargs):
    """
    Update cached building whole
    """
    building = None
    if sender is Room:
        building = instance.building
    elif sender is Zone:
        building = instance.building
    else:
        building = instance
    building.whole(refresh=True)


post_save.connect(update_cached_building, Room)
post_save.connect(update_cached_building, Zone)
post_save.connect(update_cached_building, Building)
post_delete.connect(update_cached_building, Room)
post_delete.connect(update_cached_building, Zone)
post_delete.connect(update_cached_building, Building)
