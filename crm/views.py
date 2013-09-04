from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView, DetailView, ListView, UpdateView
)

from braces.views import LoginRequiredMixin

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


class NoteCreateView(LoginRequiredMixin, CreateView):
    form_class = NoteForm
    model = Note

    def _get_ticket(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Ticket, pk=pk)

    def get_context_data(self, **kwargs):
        context = super(NoteCreateView, self).get_context_data(**kwargs)
        context.update(dict(
            ticket=self._get_ticket(),
        ))
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.ticket = self._get_ticket()
        self.object.user = self.request.user
        return super(NoteCreateView, self).form_valid(form)


class NoteUpdateView(LoginRequiredMixin, UpdateView):
    form_class = NoteForm
    model = Note

    def get_context_data(self, **kwargs):
        context = super(NoteUpdateView, self).get_context_data(**kwargs)
        context.update(dict(
            ticket=self.object.ticket,
        ))
        return context


class TicketCreateView(LoginRequiredMixin, CreateView):
    form_class = TicketForm
    model = Ticket

    def _get_contact(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Contact, slug=slug)

    def get_context_data(self, **kwargs):
        context = super(TicketCreateView, self).get_context_data(**kwargs)
        context.update(dict(
            contact=self._get_contact(),
        ))
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.contact = self._get_contact()
        self.object.user = self.request.user
        return super(TicketCreateView, self).form_valid(form)


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    form_class = TicketForm
    model = Ticket

    def get_context_data(self, **kwargs):
        context = super(TicketUpdateView, self).get_context_data(**kwargs)
        context.update(dict(
            contact=self.object.contact,
        ))
        return context


class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket

    def get_object(self, *args, **kwargs):
        obj = super(TicketDetailView, self).get_object(*args, **kwargs)
        if not self.request.user.usercontact_set.filter(contact__ticket=obj):
            raise PermissionDenied()
        return obj
