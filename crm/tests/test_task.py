import pytest

from crm.models import Task
from .factories import TaskFactory


@pytest.mark.django_db
def test_str():
    task = TaskFactory()
    str(task)


@pytest.mark.django_db
def test_due_date():
    task = TaskFactory(recurrence=Task.END_OF_MONTH)
    str(task)
