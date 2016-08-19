# -*- encoding: utf-8 -*-
import pytest

from crm.management.commands import init_app_crm


@pytest.mark.django_db
def test_init_app():
    """ Test the management command """
    command = init_app_crm.Command()
    command.handle()
