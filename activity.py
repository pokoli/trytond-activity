#This file is part of activity module for Tryton. The COPYRIGHT file at
#the top level of this repository contains the full copyright notices and
#license terms.

from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import Pool
from trytond.transaction import Transaction

import datetime

__all__ = ['ActivityReference', 'Activity']



class ActivityReference(ModelSQL, ModelView):
    'Activity Reference'
    __name__ = "activity.reference"

    model = fields.Many2One('ir.model', 'Model', required=True)


class Activity(ModelSQL, ModelView):
    'Activity'
    __name__ = "activity.activity"

    type = fields.Selection([
        ('call', 'Call'),
        ('meeting', 'Meeting'),
        ('email', 'Email'),
        ], 'Type', required=True)

    subject = fields.Char('Subject', required=True)
    resource = fields.Reference('Resource', selection='get_resource')
    dtstart = fields.DateTime('Start Date', required=True, select=True)
    dtend = fields.DateTime('End Date', select=True)
    state = fields.Selection('get_state', 'State', required=True)
    description = fields.Text('Description', required=True)
    employee = fields.Many2One('company.employee', 'Employee', required=True)
    direction = fields.Selection([
        ('incoming', 'Incoming'),
        ('outgoing', 'Outgoing'),
        ], 'Direction', required=True)
    location = fields.Char('Location')
    party = fields.Many2One('party.party', 'Party',
        on_change_with=['resource'])

    @classmethod
    def __setup__(cls):
        super(Activity, cls).__setup__()
        cls._order.insert(0, ('dtstart', 'DESC'))
        cls._order.insert(1, ('subject', 'DESC'))

    def on_change_with_party(self, name=None):

        if self.resource is None:
            return None

        model = self.resource and str(self.resource).partition(',')[0]
        Relation = Pool().get(model)
        if model == 'party.party':
            return self.resource.id
        if 'party' in Relation._fields.keys():
            if self.resource.party:
                return self.resource.party.id
        return None

    @staticmethod
    def default_dtstart():
        return datetime.datetime.now()

    @staticmethod
    def default_employee():
        User = Pool().get('res.user')
        user = User(Transaction().user)
        return user.employee and user.employee.id or None

    @staticmethod
    def default_state():
        return 'planned'

    @staticmethod
    def default_direction():
        return 'incoming'

    @staticmethod
    def default_resource():
        return None

    @staticmethod
    def get_state():
        return [
            ('planned', 'Planned'),
            ('held', 'Held'),
            ('not_held', 'Not Held'),
            ]

    @classmethod
    def get_resource(cls):
        'Return list of Model names for resource Reference'
        ActivityType = Pool().get('activity.reference')
        res = [(None, '')]
        for _type in ActivityType.search([]):
            res.append((_type.model.model, _type.model.name))
        return res
