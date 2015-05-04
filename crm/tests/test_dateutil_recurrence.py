# -*- encoding: utf-8 -*-
from datetime import date

from dateutil.rrule import (
    DAILY,
    rrule,
    TH,
    TU,
)


def test_intro():
    result = rrule(
        DAILY,
        count=3,
        byweekday=(TU, TH),
        dtstart=date(2015, 1, 1)
    )
    print('test_intro')
    for r in result:
        print(r)


def test_monthly():
    result = rrule(
        DAILY,
        count=4,
        bymonthday=(-1,),
        dtstart=date(2015, 1, 1)
    )
    print('test_monthly')
    for r in result:
        print(r)


def test_today():
    result = rrule(
        DAILY,
        count=4,
        bymonthday=(-1,),
    )
    print('test_today')
    for r in result:
        print(r)
