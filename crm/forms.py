from django import forms

from .models import (
    Contact,
    Note,
    Ticket,
)


class ContactForm(forms.ModelForm):

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


class NoteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        for name in ('name', 'description'):
            self.fields[name].widget.attrs.update(
                {'class': 'pure-input-2-3'}
            )

    class Meta:
        model = Note
        fields = (
            "name",
            "description",
        )


class TicketForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        for name in ('name', 'description'):
            self.fields[name].widget.attrs.update(
                {'class': 'pure-input-2-3'}
            )

    class Meta:
        model = Ticket
        fields = (
            "name",
            "description",
            "priority",
            "due",
        )
