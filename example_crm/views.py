# -*- encoding: utf-8 -*-
from braces.views import LoginRequiredMixin
from django.views.generic import DetailView, TemplateView

from base.view_utils import BaseMixin
from crm.views import CrmContactDetailMixin


class ContactDetailView(
        LoginRequiredMixin, CrmContactDetailMixin, BaseMixin, DetailView):

    template_name = 'crm/contact_detail.html'


class HomeView(TemplateView):

    template_name = 'example/home.html'


class SettingsView(TemplateView):

    template_name = 'example/settings.html'
