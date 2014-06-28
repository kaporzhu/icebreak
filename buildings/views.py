# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from braces.views import(
    SuperuserRequiredMixin, SetHeadlineMixin, AjaxResponseMixin,
    JSONResponseMixin
)

from .mixins import BuildingMixin, RoomSuccessURLMixin
from .models import Building, Zone, Room
from icebreak.mixins import AppRequestMixin


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


class RoomsChartView(SuperuserRequiredMixin, BuildingMixin, TemplateView):
    """
    Display the all the rooms by floor
    """
    template_name = 'buildings/rooms_chart.html'

    def get_context_data(self, **kwargs):
        """
        Add rooms to the context
        """
        data = super(RoomsChartView, self).get_context_data(**kwargs)

        if hasattr(self, 'zone'):
            floors = self.zone.floors
            rooms = self.zone.room_set.all()
        elif hasattr(self, 'building'):
            floors = self.building.floors
            rooms = self.building.room_set.all()

        # group rooms by floor
        floor_rooms = {i+1: [] for i in range(floors)}
        for room in rooms:
            floor_rooms[room.floor].append(room)
        floor_rooms = [[floor, floor_rooms[floor]] for floor in sorted(floor_rooms.keys(), reverse=True)]
        data.update({'floor_rooms': floor_rooms})

        return data


class LoadBuildingView(AjaxResponseMixin, JSONResponseMixin, View):
    """
    Load whole building in JSON
    """

    def get_ajax(self, request, *args, **kwargs):
        """
        Return whole building in JSON
        """
        building = Building.objects.get(pk=request.REQUEST['building_pk'])
        return self.render_json_response(building.whole())


class LoadZonesView(AjaxResponseMixin, JSONResponseMixin, View):
    """
    Load zones for the building
    """

    def get_ajax(self, request, *args, **kwargs):
        """
        Return zones in JSON
        """
        building = Building.objects.get(pk=request.REQUEST['building_pk'])
        return self.render_json_object_response(building.zone_set.all(),
                                                fields=('name', 'floors'))


class LoadRoomsView(AjaxResponseMixin, JSONResponseMixin, View):
    """
    Load rooms in the building or building zone
    """

    def get_ajax(self, request, *args, **kwargs):
        """
        Return rooms in JSON
        """
        if request.REQUEST.get('zone_pk'):
            zone = Zone.objects.get(pk=request.REQUEST['zone_pk'])
            rooms = zone.room_set.filter(floor=request.REQUEST['floor'])
        else:
            building = Building.objects.get(pk=request.REQUEST['building_pk'])
            rooms = building.room_set.filter(floor=request.REQUEST['floor'])
        return self.render_json_object_response(rooms, fields=('number'))


class AppGetBuildingsView(AppRequestMixin, JSONResponseMixin, View):
    """
    Get all buildings for the shop
    """
    def get(self, request, *args, **kwargs):
        buildings = self.staff.shop.building_set.all()
        buildings_json = []
        for building in buildings:
            buildings_json.append({
                'id': building.id,
                'name': building.name
            })
        return self.render_json_response(buildings_json)
