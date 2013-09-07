from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from braces.views import (
    LoginRequiredMixin,
    StaffuserRequiredMixin,
)

from .forms import (
    ContactForm,
    NoteForm,
    TicketForm,
)
from .models import (
    Contact,
    Note,
    Ticket,
    UserContact,
)
from base.view_utils import BaseMixin


class CheckPermMixin(object):

    def _check_perm(self, contact):
        if self.request.user.is_staff:
            pass
        # check the user is linked to the contact
        elif not self.request.user.usercontact_set.filter(contact=contact):
            raise PermissionDenied()


class ContactCreateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, CreateView):
    form_class = ContactForm
    model = Contact


class ContactDetailView(
        LoginRequiredMixin, CheckPermMixin, BaseMixin, DetailView):

    model = Contact

    def get_object(self, *args, **kwargs):
        obj = super(ContactDetailView, self).get_object(*args, **kwargs)
        self._check_perm(obj)
        return obj


class ContactListView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, ListView):

    model = Contact


class ContactUpdateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = ContactForm
    model = Contact


class HomeTicketListView(LoginRequiredMixin, BaseMixin, ListView):

    def get_queryset(self):
        if self.request.user.is_staff:
            result = Ticket.objects.filter(
                complete__isnull=True
            )
        else:
            try:
                contact = UserContact.objects.get(user=self.request.user)
                result = Ticket.objects.filter(
                    contact=contact, complete__isnull=True
                )
            except UserContact.DoesNotExist:
                result = Ticket.objects.none()
        return result


class NoteCreateView(
        LoginRequiredMixin, CheckPermMixin, BaseMixin, CreateView):

    form_class = NoteForm
    model = Note

    def _get_ticket(self):
        pk = self.kwargs.get('pk')
        ticket = get_object_or_404(Ticket, pk=pk)
        self._check_perm(ticket.contact)
        return ticket

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


class NoteUpdateView(
        LoginRequiredMixin, CheckPermMixin, BaseMixin, UpdateView):

    form_class = NoteForm
    model = Note

    def get_context_data(self, **kwargs):
        context = super(NoteUpdateView, self).get_context_data(**kwargs)
        self._check_perm(self.object.ticket.contact)
        context.update(dict(
            ticket=self.object.ticket,
        ))
        return context


class TicketCompleteView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, DeleteView):

    model = Ticket

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.set_complete(self.request.user)
        self.object.save()
        messages.info(
            self.request,
            "Ticket {}, {} completed on {}".format(
                self.object.pk,
                self.object.name,
                self.object.complete.strftime('%d/%m/%Y at %H:%M'),
            )
        )
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.object.contact.get_absolute_url()


class TicketCreateView(
        LoginRequiredMixin, CheckPermMixin, BaseMixin, CreateView):

    form_class = TicketForm
    model = Ticket

    def _get_contact(self):
        slug = self.kwargs.get('slug')
        contact = get_object_or_404(Contact, slug=slug)
        self._check_perm(contact)
        return contact

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


class TicketDetailView(
        LoginRequiredMixin, CheckPermMixin, BaseMixin, DetailView):

    model = Ticket

    def get_object(self, *args, **kwargs):
        obj = super(TicketDetailView, self).get_object(*args, **kwargs)
        self._check_perm(obj.contact)
        return obj


class TicketUpdateView(
        LoginRequiredMixin, CheckPermMixin, BaseMixin, UpdateView):

    form_class = TicketForm
    model = Ticket

    def get_context_data(self, **kwargs):
        context = super(TicketUpdateView, self).get_context_data(**kwargs)
        self._check_perm(self.object.contact)
        context.update(dict(
            contact=self.object.contact,
        ))
        return context
