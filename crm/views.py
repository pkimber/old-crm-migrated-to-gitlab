# -*- encoding: utf-8 -*-
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
from rest_framework import (
    authentication,
    permissions,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from base.view_utils import BaseMixin
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
from .serializers import TicketSerializer


def check_perm(user, contact):
    if user.is_staff:
        pass
    elif user.usercontact.contact == contact:
        pass
    else:
        # the user is NOT linked to the contact
        raise PermissionDenied()


class CheckPermMixin(object):

    def _check_perm(self, contact):
        check_perm(self.request.user, contact)


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

    paginate_by = 20

    model = Contact


class ContactUpdateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = ContactForm
    model = Contact


class HomeTicketListView(LoginRequiredMixin, BaseMixin, ListView):

    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(HomeTicketListView, self).get_context_data(**kwargs)
        context.update(dict(
            is_home=True,
        ))
        return context

    def get_queryset(self):
        if self.request.user.is_staff:
            result = Ticket.objects.filter(
                complete__isnull=True,
                priority__level__gt=0,
                user_assigned=self.request.user,
            )
        else:
            try:
                user_contact = UserContact.objects.get(user=self.request.user)
                result = Ticket.objects.filter(
                    contact=user_contact.contact,
                    complete__isnull=True,
                )
            except UserContact.DoesNotExist:
                result = Ticket.objects.none()
        return result


class NoteCreateView(
        LoginRequiredMixin, CheckPermMixin, BaseMixin, CreateView):

    form_class = NoteForm
    model = Note

    def _get_ticket(self):
        pk = self.kwargs.get('pk', None)
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


class ProjectTicketDueListView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, ListView):

    paginate_by = 30
    template_name = 'crm/project_ticket_list.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectTicketDueListView, self).get_context_data(**kwargs)
        context.update(dict(
            sort_by_due_date=True,
        ))
        return context

    def get_queryset(self):
        return Ticket.objects.current().order_by('due', 'priority')


class ProjectTicketPriorityListView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, ListView):

    paginate_by = 30
    template_name = 'crm/project_ticket_list.html'

    def get_queryset(self):
        return Ticket.objects.current().order_by('priority', 'due')


class TicketAPIView(APIView):

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    #permission_classes = (permissions.AllowAny,)

    def get(self, request, pk=None, format=None):
        if pk:
            ticket = Ticket.objects.get(pk=pk)
            serializer = TicketSerializer(ticket)
        else:
            serializer = TicketSerializer(
                Ticket.objects.planner().order_by('pk'),
                many=True
            )
        return Response(serializer.data)


class TicketCompleteView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, DeleteView):

    model = Ticket

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.set_complete(self.request.user)
        self.object.save()
        messages.info(
            self.request,
            "Completed ticket {}, {} on {}".format(
                self.object.pk,
                self.object.title,
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
        slug = self.kwargs.get('slug', None)
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
        obj = super().get_object(*args, **kwargs)
        self._check_perm(obj.contact)
        return obj


class TicketListView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, ListView):

    paginate_by = 20

    def get_queryset(self):
        return Ticket.objects.filter(
            complete__isnull=True
        ).order_by(
            'due',
            'priority',
        )


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
