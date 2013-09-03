from django import forms

from .models import Ticket


class TicketForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        #self.fields['name'].widget.attrs.update({'class': 'pure-input-1-2'})
        #self.fields['description'].widget.attrs.update({'class': 'pure-input-1-2'})
        #self.fields['priority'].widget.attrs.update({'class': 'pure-input-2-3'})
        #self.fields['date_due'].widget.attrs.update({'class': 'pure-input-2-3'})

    class Meta:
        model = Ticket
        fields = (
            "name",
            "description",
            "priority",
            "date_due",
        )
