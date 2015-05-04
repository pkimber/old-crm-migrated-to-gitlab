# -*- encoding: utf-8 -*-
from django import forms

from base.form_utils import RequiredFieldForm
from .models import (
    Contact,
    Note,
    Task,
    Ticket,
)


class ContactForm(RequiredFieldForm):

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        for name in ('name', 'address', 'mail', 'url', 'industry'):
            self.fields[name].widget.attrs.update(
                {'class': 'pure-input-2-3'}
            )

    class Meta:
        model = Contact
        fields = (
            "name",
            "address",
            "slug",
            "url",
            "phone",
            "mail",
            "industry",
            "hourly_rate",
        )


class NoteForm(RequiredFieldForm):

    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        for name in ('title', 'description'):
            self.fields[name].widget.attrs.update(
                {'class': 'pure-input-2-3'}
            )

    class Meta:
        model = Note
        fields = (
            "title",
            "description",
        )


class TaskEmptyForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ()


class TaskForm(RequiredFieldForm):

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        for name in ('title', 'description'):
            self.fields[name].widget.attrs.update(
                {'class': 'pure-input-2-3'}
            )

    class Meta:
        model = Task
        fields = (
            'title',
            'recurrence',
            'description',
            'user_assigned',
        )


class TicketForm(RequiredFieldForm):

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        for name in ('title', 'description'):
            self.fields[name].widget.attrs.update(
                {'class': 'pure-input-2-3'}
            )

    class Meta:
        model = Ticket
        fields = (
            "priority",
            "title",
            "description",
            "due",
            "user_assigned",
        )
