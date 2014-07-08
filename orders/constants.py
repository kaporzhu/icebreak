# -*- coding: utf-8 -*-
from datetime import time


# order status
UNPAID = 'unpaid'
PAID = 'paid'
PRINTED = 'printed'
PACKING_DONE = 'packing done'
ON_THE_WAY = 'on the way'
DISTRIBUTING = 'distributing'
DONE = 'done'

STATUSES = [UNPAID, PAID, PRINTED, PACKING_DONE, ON_THE_WAY, DISTRIBUTING, DONE]  # noqa

ORDER_STEPS = {
    UNPAID: {
        'label': u'下单',
        'date': '',
        'time': '',
        'is_done': True
    },
    PAID: {
        'label': u'付款',
        'date': '',
        'time': '',
        'is_done': False
    },
    PRINTED: {
        'label': u'打印订单',
        'date': '',
        'time': '',
        'is_done': False
    },
    PACKING_DONE: {
        'label': u'打包完成',
        'date': '',
        'time': '',
        'is_done': False
    },
    ON_THE_WAY: {
        'label': u'配送员出发',
        'date': '',
        'time': '',
        'is_done': False
    },
    DISTRIBUTING: {
        'label': u'到达写字楼',
        'date': '',
        'time': '',
        'is_done': False
    },
    DONE: {
        'label': u'完成',
        'date': '',
        'time': '',
        'is_done': False
    }
}

# order delivery time
DELIVERY_TIMES = [
    {
        'time': '11:00-11:45',
        'cutoff_time': time(10, 40)
    },
    {
        'time': '11:45-12:30',
        'cutoff_time': time(11, 25)
    },
    {
        'time': '12:30-13:00',
        'cutoff_time': time(12, 10)
    },
    {
        'time': u'13:00之后',
        'cutoff_time': time(23, 00)
    }
]

DISCOUNTS = [0, 0, 0.01, 0.02, 0.03, 0.04, 0.05]
