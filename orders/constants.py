# -*- coding: utf-8 -*-
from datetime import time


# order status
UNPAID = 'unpaid'
PAID = 'paid'
PACKING_DONE = 'packing done'
ON_THE_WAY = 'on the way'
DISTRIBUTING = 'distributing'
DONE = 'done'

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
