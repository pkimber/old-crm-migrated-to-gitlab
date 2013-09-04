from django import forms

from .models import (
    Note,
    Ticket,
)


class NoteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update(
            {'class': 'pure-input-2-3'}
        )

    class Meta:
        model = Note
        fields = (
            "description",
        )


class TicketForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'pure-input-2-3'})
        self.fields['description'].widget.attrs.update(
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
