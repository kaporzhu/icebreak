# -*- coding: utf-8 -*-
from .constants import WAITING
from .models import SMSNotification


def send_sms_async(phone, content):
    """
    Create new SMS notification object
    """
    SMSNotification(phone=phone, content=content, status=WAITING).save()
