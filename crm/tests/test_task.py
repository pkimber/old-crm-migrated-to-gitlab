# -*- encoding: utf-8 -*-
import pytest

from dateutil.relativedelta import relativedelta

from django.utils import timezone

from crm.models import Task
from .factories import TaskFactory


@pytest.mark.django_db
def test_str():
    task = TaskFactory()
    str(task)


@pytest.mark.django_db
def test_recurrence_init():
    task = TaskFactory(recurrence=Task.END_OF_MONTH)
    task.recurrence_init()
    last_day_of_this_month = timezone.now() + relativedelta(
        months=+1, day=1, days=-1
    )
    assert last_day_of_this_month.date() == task.due.date()


@pytest.mark.django_db
def test_recurrence_increment():
    task = TaskFactory(recurrence=Task.END_OF_MONTH)
    task.recurrence_init()
    task.recurrence_increment()
    last_day_of_next_month = timezone.now() + relativedelta(
        months=+2, day=1, days=-1
    )
    assert last_day_of_next_month.date() == task.due.date()
