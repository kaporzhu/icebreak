# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from braces.views import(
    SuperuserRequiredMixin, SetHeadlineMixin
)

from .mixins import BuildingMixin, RoomSuccessURLMixin
from .models import Building, Zone, Room


class CreateBuildingView(SuperuserRequiredMixin, SetHeadlineMixin, CreateView):
    """
    Create new Building
    """
    model = Building
    headline = u'添加新楼'
    success_url = reverse_lazy('buildings:list')


class UpdateBuildingView(SuperuserRequiredMixin, SetHeadlineMixin, UpdateView):
    """
    Update Building info
    """
    model = Building
    headline = u'更新写字楼信息'
    success_url = reverse_lazy('buildings:list')


class BuildingListView(SuperuserRequiredMixin, ListView):
    """
    Display all Buildings for admin
    """
    model = Building


class CreateZoneView(SuperuserRequiredMixin, SetHeadlineMixin, BuildingMixin,
                     CreateView):
    """
    Create new Building zone
    """
    model = Zone
    headline = u'添加分区'
    success_url = reverse_lazy('buildings:list')

    def get_initial(self):
        """
        Initial data for form
        """
        return {'building': self.building}


class UpdateZoneView(SuperuserRequiredMixin, SetHeadlineMixin, BuildingMixin,
                     UpdateView):
    """
    Update Building zone info
    """
    model = Zone
    headline = u'更新分区信息'
    success_url = reverse_lazy('buildings:list')


class CreateRoomView(SuperuserRequiredMixin, SetHeadlineMixin, BuildingMixin,
                     RoomSuccessURLMixin, CreateView):
    """
    Create new Building room
    """
    model = Room
    headline = u'添加办公室'

    def get_initial(self):
        """
        Initial data for form
        """
        initial = super(CreateRoomView, self).get_initial()
        if hasattr(self, 'building'):
            initial.update({'building': self.building})
        if hasattr(self, 'zone'):
            initial.update({'zone': self.zone})

        return initial

    def get_form(self, form_class):
        """
        Limit zone field
        """
        form = super(CreateRoomView, self).get_form(form_class)
        form.fields['zone'].queryset = self.building.zone_set.all()
        return form


class UpdateRoomView(SuperuserRequiredMixin, SetHeadlineMixin, BuildingMixin,
                     RoomSuccessURLMixin, UpdateView):
    """
    Update Building room
    """
    model = Room
    headline = u'更新办公室信息'


class DeleteRoomView(SuperuserRequiredMixin, BuildingMixin,
                     RoomSuccessURLMixin, DeleteView):
    """
    Update Building room
    """
    model = Room


class RoomListView(SuperuserRequiredMixin, BuildingMixin, SetHeadlineMixin,
                   ListView):
    """
    Display all the rooms in the building or building zone
    """
    model = Room

    def get_headline(self):
        headline = self.building.name
        if hasattr(self, 'zone'):
            headline += self.zone.name
        headline += u'的所有办公室'

        return headline

    def get_queryset(self):
        """
        Filter rooms
        """
        qs = super(RoomListView, self).get_queryset()
        if hasattr(self, 'zone'):
            qs = qs.filter(zone=self.zone)
        elif hasattr(self, 'building'):
            qs = qs.filter(building=self.building)

        return qs.order_by('floor')
