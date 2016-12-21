# -*- encoding: utf-8 -*-
from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
)
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from base.view_utils import BaseMixin
from contact.views import ContactDetailMixin, ContactUpdateMixin
from crm.service import get_contact_model
from invoice.forms import QuickTimeRecordEmptyForm
from invoice.models import QuickTimeRecord, TimeRecord
from .forms import CrmContactForm, NoteForm, TicketForm
from .models import CrmContact, CrmError, Note, Ticket
from .serializers import TicketSerializer


class CrmContactCreateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, CreateView):

    model = CrmContact
    form_class = CrmContactForm

    def _contact(self):
        pk = self.kwargs.get('pk')
        contact = get_contact_model().objects.get(pk=pk)
        return contact

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.contact = self._contact()
        return super().form_valid(form)


class CrmContactDetailMixin(ContactDetailMixin):

    def _ticket_list(self):
        return Ticket.objects.contact(self.object).order_by(
            '-complete',
            'due',
            'priority',
            'created',
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # crm
        try:
            crm_contact = self.object.crmcontact
        except ObjectDoesNotExist:
            crm_contact = None
        # invoice
        try:
            invoice_contact = self.object.invoicecontact
        except ObjectDoesNotExist:
            invoice_contact = None
        context.update(dict(
            crm_contact=crm_contact,
            invoice_contact=invoice_contact,
            ticket_list=self._ticket_list(),
        ))
        return context


class CrmContactUpdateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    model = CrmContact
    form_class = CrmContactForm


class HomeTicketListView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, ListView):

    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
            # try:
            #     user_contact = UserContact.objects.get(user=self.request.user)
            #     result = Ticket.objects.filter(
            #         contact=user_contact.contact,
            #         complete__isnull=True,
            #     )
            # except UserContact.DoesNotExist:
            #     result = Ticket.objects.none()
            result = Ticket.objects.none()
        return result


class NoteCreateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, CreateView):

    form_class = NoteForm
    model = Note

    def _get_ticket(self):
        pk = self.kwargs.get('pk', None)
        ticket = get_object_or_404(Ticket, pk=pk)
        return ticket

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(dict(
            ticket=self._get_ticket(),
        ))
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.ticket = self._get_ticket()
        self.object.user = self.request.user
        return super().form_valid(form)


class NoteUpdateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = NoteForm
    model = Note

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(dict(
            ticket=self.object.ticket,
        ))
        return context


class ProjectTicketDueListView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, ListView):

    paginate_by = 30
    template_name = 'crm/project_ticket_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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


class TicketChildCreateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, CreateView):

    form_class = TicketForm
    model = Ticket

    def _ticket(self):
        pk = self.kwargs.get('pk', None)
        ticket = Ticket.objects.get(pk=pk)
        return ticket

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(dict(
            ticket=self._ticket(),
        ))
        return context

    def form_valid(self, form):
        ticket = self._ticket()
        self.object = form.save(commit=False)
        self.object.contact = ticket.contact
        self.object.parent = ticket
        self.object.user = self.request.user
        return super().form_valid(form)


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
        return reverse('contact.detail', args=[self.object.contact.pk])


class TicketCreateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, CreateView):

    form_class = TicketForm
    model = Ticket

    def _contact(self):
        pk = self.kwargs.get('pk')
        contact = get_contact_model().objects.get(pk=pk)
        return contact

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(dict(
            contact=self._contact(),
        ))
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.contact = self._contact()
        self.object.user = self.request.user
        return super().form_valid(form)


class TicketDetailView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, FormView):

    form_class = QuickTimeRecordEmptyForm
    template_name = 'crm/ticket_detail.html'

    def _ticket(self):
        pk = self.kwargs.get('pk')
        ticket = Ticket.objects.get(pk=pk)
        return ticket

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(dict(
            ticket=self._ticket(),
            quick=QuickTimeRecord.objects.quick(self.request.user),
        ))
        return context

    def form_valid(self, form):
        quick_pk = self.request.POST.get('quick')
        ticket = self._ticket()
        try:
            quick_time_record = QuickTimeRecord.objects.get(pk=quick_pk)
        except QuickTimeRecord.DoesNotExist:
            raise CrmError(
                "Cannot find quick time record '{}'".format(quick_pk)
            )
        TimeRecord.objects.start(ticket, quick_time_record)
        return HttpResponseRedirect(
            reverse('crm.ticket.detail', args=[ticket.pk])
        )


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
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = TicketForm
    model = Ticket

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(dict(
            contact=self.object.contact,
        ))
        return context
