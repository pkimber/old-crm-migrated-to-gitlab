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
            result = Ticket.objects.all()
        else:
            result = Ticket.objects.filter(
                contact__usercontact__user__in=(self.request.user,)
            )
        return result


class TicketCreateView(LoginRequiredMixin, CreateWithRelatedMixin, CreateView):
    form_class = TicketForm
    model = Ticket
    related_model = Contact


class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
