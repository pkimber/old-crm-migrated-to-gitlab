from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView, DetailView, ListView,
)

from braces.views import LoginRequiredMixin

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


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note

    def _get_ticket_pk(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Ticket, pk=pk)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.company = self._get_ticket_pk()
        self.object.user = self.request.user
        return super(NoteCreateView, self).form_valid(form)


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket

    def _get_contact_slug(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Contact, slug=slug)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.company = self._get_contact_slug()
        self.object.user = self.request.user
        return super(TicketCreateView, self).form_valid(form)


class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
