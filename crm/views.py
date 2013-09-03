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

    #def _get_contact(self):
    #    slug = self.kwargs.get('slug')
    #    return get_object_or_404(Invoice, pk=invoice_id)

    #def form_valid(self, form):
    #    self.object = form.save(commit=False)
    #    self.object.invoice = self._get_invoice()
    #    return super(InvoiceLineCreateView, self).form_valid(form)


class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
