from django.views.generic import (
    CreateView, DetailView, ListView,
)

from braces.views import LoginRequiredMixin
from related.views import CreateWithRelatedMixin

from .forms import (
    TicketForm,
)
from .models import (
    Contact,
    Ticket,
)


class ContactDetailView(LoginRequiredMixin, DetailView):
    model = Contact


class HomeListView(LoginRequiredMixin, ListView):

    def get_queryset(self):
        if self.request.user.is_staff:
            result = Contact.objects.all()
        else:
            result = self.request.user.contact_set.all()
        return result


class TicketCreateView(LoginRequiredMixin, CreateWithRelatedMixin, CreateView):
    form_class = TicketForm
    model = Ticket
    related_model = Contact


class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
