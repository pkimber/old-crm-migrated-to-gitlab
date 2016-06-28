# -*- encoding: utf-8 -*-
from django.conf import settings
from django.apps import apps


def get_contact_model():
    return apps.get_model(settings.CONTACT_MODEL)
