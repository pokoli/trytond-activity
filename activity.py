# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import datetime

from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import Pool
from trytond.transaction import Transaction

__all__ = ['ActivityReference', 'Activity']


class ActivityReference(ModelSQL, ModelView):
    'Activity Reference'
    __name__ = "activity.reference"

    model = fields.Many2One('ir.model', 'Model', required=True)


class Activity(ModelSQL, ModelView):
    'Activity'
    __name__ = "activity.activity"
    _rec_name = 'subject'

    type = fields.Selection([
        ('call', 'Call'),
        ('meeting', 'Meeting'),
        ('email', 'Email'),
        ], 'Type', required=True)

    subject = fields.Char('Subject', required=True)
    resource = fields.Reference('Resource', selection='get_resource')
    dtstart = fields.DateTime('Start Date', required=True, select=True)
    dtend = fields.DateTime('End Date', select=True)
    state = fields.Selection([
            ('planned', 'Planned'),
            ('held', 'Held'),
            ('not_held', 'Not Held'),
            ], 'State', required=True)
    description = fields.Text('Description')
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
        return Activity._resource_party(self.resource)

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

    @classmethod
    def default_party(cls):
        resource = cls.default_resource()
        return Activity._resource_party(resource)

    @staticmethod
    def _resource_party(resource):
        if resource is None or resource.id < 0:
            return None

        model = resource and str(resource).partition(',')[0]
        Relation = Pool().get(model)
        if model == 'party.party':
            return resource.id
        if 'party' in Relation._fields.keys():
            if resource.party:
                return resource.party.id
        return None

    @classmethod
    def get_resource(cls):
        'Return list of Model names for resource Reference'
        ActivityType = Pool().get('activity.reference')
        res = [(None, '')]
        for _type in ActivityType.search([]):
            res.append((_type.model.model, _type.model.name))
        return res
