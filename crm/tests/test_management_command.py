# -*- encoding: utf-8 -*-
import pytest

from django.test import TestCase

from crm.management.commands import init_app_crm
from login.management.commands import demo_data_login


@pytest.mark.django_db
def test_init_app():
    """ Test the management command """
    command = init_app_crm.Command()
    command.handle()
