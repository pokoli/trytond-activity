#This file is part of activity module for Tryton. The COPYRIGHT file at
#the top level of this repository contains the full copyright notices and
#license terms.

from trytond.model import fields
from trytond.pool import PoolMeta


__all__ = ['Party']

__metaclass__ = PoolMeta


class Party:
    'Party'
    __name__ = "Party"

    activities = fields.One2Many('activity.activity', 'party',
        'Activities')

