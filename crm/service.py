# -*- encoding: utf-8 -*-
from django.conf import settings
from django.db.models.loading import get_model


def get_contact_model():
    return get_model(settings.CONTACT_MODEL)
