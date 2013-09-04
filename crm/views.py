from django.views.generic import (
    CreateView, DetailView, ListView,
)

from braces.views import LoginRequiredMixin
from related.views import CreateWithRelatedMixin

from .forms import (
    NoteForm,
    TicketForm,
)
from .models import (
    Contact,
    Note,
    Ticket,
    UserContact,
)


class ContactDetailView(LoginRequiredMixin, DetailView):
    model = Contact


class HomeListView(LoginRequiredMixin, ListView):

    def get_queryset(self):
        if self.request.user.is_staff:
            result = Ticket.objects.all()
        else:
            contact = UserContact.objects.get(user=self.request.user)
            result = Ticket.objects.filter(contact=contact)
        return result


class NoteCreateView(LoginRequiredMixin, CreateWithRelatedMixin, CreateView):
    form_class = NoteForm
    model = Note
    related_model = Ticket


class TicketCreateView(LoginRequiredMixin, CreateWithRelatedMixin, CreateView):
    form_class = TicketForm
    model = Ticket
    related_model = Contact


class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
