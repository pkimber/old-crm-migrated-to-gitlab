# -*- encoding: utf-8 -*-
import pytest

from datetime import date, time
from django.utils import timezone

from contact.tests.factories import ContactFactory
from crm.models import Ticket
from crm.tests.factories import TicketFactory
from invoice.tests.factories import TimeRecordFactory, InvoiceLineFactory
from search.tests.helper import check_search_methods


@pytest.mark.django_db
def test_contact():
    contact = ContactFactory()
    TicketFactory(contact=contact, due=date.today(), title='t1')
    TicketFactory(contact=contact, title='t2')
    TicketFactory(contact=contact, complete=timezone.now(), title='t3')
    TicketFactory(title='t4')
    qs = Ticket.objects.contact(contact)
    assert ['t3', 't2', 't1'] == [obj.title for obj in qs]


@pytest.mark.django_db
def test_due():
    ticket = TicketFactory(due=date.today())
    assert not ticket.is_overdue


@pytest.mark.django_db
def test_overdue():
    ticket = TicketFactory(due=date(2010, 1, 1))
    assert ticket.is_overdue


@pytest.mark.django_db
def test_search_methods():
    check_search_methods(TicketFactory())


@pytest.mark.django_db
def test_str():
    str(TicketFactory())


@pytest.mark.django_db
def test_ticket_totals():
    start_date = date(day=3, month=2, year=2017)
    ticket = TicketFactory()
    """
    This loop generates the following timerecords:
    Date       Start Tm End Tm   Delta   Billable Invoice Line
    2017-02-03 01:01:00 01:02:00 0:01:00 False    None
    2017-02-03 02:02:00 02:05:00 0:03:00 True     None
    2017-02-03 03:03:00 03:10:00 0:07:00 False    None
    2017-02-03 04:04:00 04:17:00 0:13:00 True     None
    2017-02-03 05:05:00 05:26:00 0:21:00 False    None
    2017-02-03 06:06:00 06:37:00 0:31:00 True     0 1.00 description_0 @0.00
    2017-02-03 08:00:00 None     0:00:00 True     None
    """
    for t in range(1, 7):
        start_time = time(hour=t, minute=t)
        end_time = time(hour=t, minute=t*t+1)
        tr = TimeRecordFactory(
            ticket=ticket, date_started=start_date, start_time=start_time,
            end_time=end_time, billable=t % 2 == 0,
        )
    # make the last time record invoiced
    tr.invoice_line = InvoiceLineFactory(timerecord=tr)
    tr.save()
    # open time record - should be ignored
    TimeRecordFactory(
        ticket=ticket, date_started=start_date, start_time=time(hour=8),
        end_time=None, billable=True,
    )
    totals = ticket.totals()
    assert str(totals['total']) == '1:16:00'
    assert str(totals['not_billable']) == '0:29:00'
    assert str(totals['pending']) == '0:16:00'
    assert str(totals['billable']) == '0:47:00'
    assert str(totals['invoiced']) == '0:31:00'
