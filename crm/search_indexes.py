# -*- encoding: utf-8 -*-
from celery_haystack.indexes import CelerySearchIndex

from haystack import indexes

from .models import (
    # Contact,
    Note,
    Ticket,
)


# class ContactIndex(CelerySearchIndex, indexes.Indexable):
#
#     text = indexes.CharField(document=True, use_template=True)
#
#     def get_model(self):
#         return Contact


class NoteIndex(CelerySearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Note


class TicketIndex(CelerySearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Ticket
