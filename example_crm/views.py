# -*- encoding: utf-8 -*-
from braces.views import LoginRequiredMixin
from django.views.generic import DetailView, TemplateView

from base.view_utils import BaseMixin
from contact.views import ContactDetailMixin


class ContactDetailView(
        LoginRequiredMixin, ContactDetailMixin, BaseMixin, DetailView):
    pass


class HomeView(TemplateView):

    template_name = 'example/home.html'


class SettingsView(TemplateView):

    template_name = 'example/settings.html'
