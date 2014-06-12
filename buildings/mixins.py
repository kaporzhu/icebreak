# -*- coding: utf-8 -*-
from .models import Building, Zone
from django.core.urlresolvers import reverse_lazy


class BuildingMixin(object):
    """
    Mixin for buildings app views
    """
    def dispatch(self, request, *args, **kwargs):
        """
        If building_pk is existed, set building to current object.
        If zone_pk is existed, set building to current object.
        """
        if kwargs.get('building_pk'):
            self.building = Building.objects.get(pk=kwargs['building_pk'])
        if kwargs.get('zone_pk'):
            self.zone = Zone.objects.get(pk=kwargs['zone_pk'])
        return super(BuildingMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Add building and zone to the context
        """
        data = super(BuildingMixin, self).get_context_data(**kwargs)
        if hasattr(self, 'building'):
            data.update({'building': self.building})
        if hasattr(self, 'zone'):
            data.update({'zone': self.zone})

        return data


class RoomSuccessURLMixin(object):
    """
    Mixin for room views
    """

    def get_success_url(self):
        if self.kwargs['zone_pk']:
            return reverse_lazy('buildings:room_list',
                                kwargs={'building_pk': self.building.id,
                                        'zone_pk': self.zone.id})
        else:
            return reverse_lazy('buildings:room_list',
                                kwargs={'building_pk': self.building.id})
