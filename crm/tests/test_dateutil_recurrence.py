# -*- encoding: utf-8 -*-
import pytz

from datetime import datetime
from dateutil.rrule import (
    MONTHLY,
    rrule,
)


def test_end_of_month():
    d = datetime(2015, 1, 10, 0, 0, 0, tzinfo=pytz.utc)
    rule = rrule(MONTHLY, bymonthday=(-1,), dtstart=d)
    result = rule.after(d)
    assert datetime(2015, 1, 31, 0, 0, 0, tzinfo=pytz.utc) == result


def test_end_of_following_month():
    d = datetime(2015, 1, 10, 0, 0, 0, tzinfo=pytz.utc)
    rule = rrule(MONTHLY, bymonthday=(-1,), dtstart=d)
    # current recurrence
    current = rule.after(d)
    # next recurrence
    result = rule.after(current)
    assert datetime(2015, 2, 28, 0, 0, 0, tzinfo=pytz.utc) == result
