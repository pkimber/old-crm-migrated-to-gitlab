# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth import get_user_model

from base.form_utils import RequiredFieldForm
from .models import CrmContact, Note, Ticket


class CrmContactForm(forms.ModelForm):

    class Meta:
        model = CrmContact
        fields = (
            "industry",
        )

# class ContactForm(RequiredFieldForm):
#
#     def __init__(self, *args, **kwargs):
#         super(ContactForm, self).__init__(*args, **kwargs)
#         for name in ('name', 'address', 'mail', 'url', 'industry'):
#             self.fields[name].widget.attrs.update(
#                 {'class': 'pure-input-2-3'}
#             )
#
#     class Meta:
#         model = Contact
#         fields = (
#             "name",
#             "address",
#             "slug",
#             "url",
#             "phone",
#             "mail",
#             "industry",
#             "hourly_rate",
#         )


class NoteForm(RequiredFieldForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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


class TicketForm(RequiredFieldForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ('title', 'description'):
            self.fields[name].widget.attrs.update(
                {'class': 'pure-input-2-3'}
            )
        qs = get_user_model().objects.filter(
            is_active=True,
            is_staff=True,
        ).order_by(
            'username'
        )
        f = self.fields['user_assigned']
        f.queryset = qs
        f.label_from_instance = user_label_from_instance

    class Meta:
        model = Ticket
        fields = (
            "priority",
            "title",
            "description",
            "due",
            "user_assigned",
        )


def user_label_from_instance(obj):
    result = obj.get_full_name()
    if not result:
        result = obj.username
    return result
