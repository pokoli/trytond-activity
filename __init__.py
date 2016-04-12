# This file is part of activity module for Tryton. The COPYRIGHT file at
# the top level of this repository contains the full copyright notices and
# license terms.
from trytond.pool import Pool
from .configuration import *
from .activity import *
from .party import *


def register():
    Pool.register(
        Configuration,
        CompanyConfiguration,
        ActivityType,
        ActivityReference,
        Activity,
        Party,
        module='activity', type_='model')
