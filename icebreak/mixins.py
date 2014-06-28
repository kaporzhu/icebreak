# -*- coding: utf-8 -*-
from django.http.response import HttpResponseForbidden

from braces.views import JSONResponseMixin

from accounts.models import Staff


class AppRequestMixin(JSONResponseMixin, object):
    """
    Mixin for all requests from app.
    Validate username and api_key first.
    """

    def dispatch(self, request, *args, **kwargs):
        """
        Check username and api_key
        """
        try:
            staff = Staff.objects.get(pk=request.REQUEST['staff_id'])
            if staff.api_key != request.REQUEST['api_key']:
                return self.render_json_response({
                    'success': False,
                    'reason': 'Api key doesn\'t match'
                })
            else:
                self.staff = staff
                return super(AppRequestMixin, self).dispatch(request, *args,
                                                             **kwargs)
        except Staff.DoesNotExist:
            return HttpResponseForbidden()
