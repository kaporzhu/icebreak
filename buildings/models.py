# -*- coding: utf-8 -*-
from datetime import datetime

from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save, post_delete

from orders.constants import DISTRIBUTING
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

    def _sort_rooms_by_floor(self, floors, rooms):
        """
        Rooms in JSON and rooms by floor in JSON
        """
        rooms_by_floor_dict = {i+1: [] for i in range(floors)}
        for room in rooms:
            rooms_by_floor_dict[room['floor']].append(room)

        rooms_by_floor_list = []
        for floor in sorted(rooms_by_floor_dict.keys(), reverse=True):
            rooms_by_floor_list.append(
                {'floor': floor, 'rooms': rooms_by_floor_dict[floor]})

        return rooms_by_floor_list

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
                whole['zones'] = {}
                for zone in self.zone_set.all():
                    zone_whole = {
                        'id': zone.id,
                        'name': zone.name,
                        'floors': zone.floors,
                        'rooms': {}
                    }
                    whole['zones'][zone.id] = zone_whole
                    for room in zone.room_set.all():
                        zone_whole['rooms'][room.id] = {
                            'id': room.id,
                            'number': room.number,
                            'floor': room.floor
                        }
            else:
                whole['rooms'] = {}
                for room in self.room_set.all():
                    whole['rooms'][room.id] = {
                        'id': room.id,
                        'number': room.number,
                        'floor': room.floor
                    }

            cache.set(cache_key, whole, 1728000)  # cache for one month

        return cache.get(cache_key)

    def whole_rooms_by_floor(self, building_whole):
        """
        Sort rooms by floor
        """
        if building_whole['is_multiple']:
            for zone_id, zone in building_whole['zones'].items():
                zone['rooms_by_floor'] = self._sort_rooms_by_floor(zone['floors'], zone['rooms'].values())  # noqa
        else:
            building_whole['rooms_by_floor'] = self._sort_rooms_by_floor(building_whole['floors'], building_whole['rooms'].values())  # noqa

        return building_whole

    def whole_with_orders(self, refersh=False):
        """
        cached building info with orders.
        """
        cache_key = 'building_whole_with_orders_{}'.format(self.id)
        if refersh or not cache.get(cache_key):
            from orders.models import Order


            now = datetime.now()
            start = datetime(now.year, now.month, now.day, 0, 0)
            end = datetime(now.year, now.month, now.day, 23, 59)
            whole = self.whole()
            for order in Order.objects.filter(building=self, status=DISTRIBUTING).filter(created_at__range=(start, end)):  # noqa
                if self.is_multiple:
                    whole['zones'][order.zone.id]['has_order'] = True
                    whole['zones'][order.zone.id]['rooms'][order.room.id].update({'status': DISTRIBUTING})
                else:
                    whole['has_order'] = True
                    whole['rooms'][order.room.id].update({'status': DISTRIBUTING})
            cache.set(cache_key, self.whole_rooms_by_floor(whole), 3600)  # cache for 1 hours

        return cache.get(cache_key)

    def update_order_status_in_whole(self, order):
        """
        Update order status for the room
        """
        cache_key = 'building_whole_with_orders_{}'.format(self.id)
        whole_with_orders = self.whole_with_orders()
        now = datetime.now().strftime('%H:%M')
        whole_with_orders['latest'] = {
            'time': now,
            'address': order.short_address,
            'floor': order.room.floor,
            'zone': order.zone.id if order.zone else None
        }
        if whole_with_orders['is_multiple']:
            for room in whole_with_orders['zones'][order.zone.id]['rooms_by_floor'][-order.room.floor]['rooms']:  # noqa
                if room['id'] == order.room.id:
                    room['status'] = order.status
                    room['delivery_time'] = now
                    break
        else:
            for room in whole_with_orders['rooms_by_floor'][-order.room.floor]['rooms']:
                if room['id'] == order.room.id:
                    room['status'] = order.status
                    room['delivery_time'] = now
                    break
        cache.set(cache_key, whole_with_orders, 10800)


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
