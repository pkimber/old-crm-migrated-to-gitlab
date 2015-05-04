import pytest

from .factories import TaskFactory


@pytest.mark.django_db
def test_str():
    task = TaskFactory()
    str(task)
