# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from icebreak.utils import send_sms
from tasks.constants import WAITING, SENDING, SENT, FAILED
from tasks.models import SMSNotification


class Command(BaseCommand):
    """
    Send SMS notification command
    """

    def handle(self, *args, **options):
        sms_notifications = list(SMSNotification.objects.filter(status=WAITING))
        SMSNotification.objects.filter(status=WAITING).update(status=SENDING)
        for sms in sms_notifications:
            success, msg = send_sms(sms.phone, sms.content)
            if success:
                sms.status = SENT
            else:
                sms.status = FAILED
                sms.failed_reason = msg
            sms.save()
