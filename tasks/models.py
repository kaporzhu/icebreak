# -*- coding: utf-8 -*-
from django.db import models

from .constants import WAITING, SENT, FAILED


class SMSNotification(models.Model):
    """
    SMS notification model
    """

    STATUS_CHOICES = (
        (WAITING, u'等待发送'),
        (SENT, u'已发送'),
        (FAILED, u'发送失败')
    )

    phone = models.CharField(max_length=16)
    content = models.CharField(max_length=128)
    status = models.CharField(max_length=16, db_index=True,
                              choices=STATUS_CHOICES)
    failed_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(auto_now_add=True)
