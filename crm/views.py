from django.views.generic import ListView

from braces.views import LoginRequiredMixin

from .models import Contact


class HomeListView(LoginRequiredMixin, ListView):

    def get_queryset(self):
        if self.request.user.is_staff:
            result = Contact.objects.all()
        else:
            result = self.request.user.contact_set.all()
        return result
