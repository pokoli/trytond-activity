# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta


__all__ = ['Party']
__metaclass__ = PoolMeta


class Party:
    __name__ = 'party.party'
    activities = fields.One2Many('activity.activity', 'party',
        'Activities')
