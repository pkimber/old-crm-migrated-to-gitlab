# -*- encoding: utf-8 -*-
import pytest

from crm.tests.factories import (
    PriorityFactory,
    TicketFactory,
)


#@pytest.mark.django_db
#def test_mptt():
#    parent = TicketFactory()
#    TicketFactory(title='1', parent=parent)
#    TicketFactory(title='2')
#    TicketFactory(title='3', parent=parent)
#    assert ['1', '3'] == [o.title for o in parent.get_children()]
