# -*- encoding: utf-8 -*-
from django.views.generic import TemplateView


class HomeView(TemplateView):

    template_name = 'example/home.html'


class SettingsView(TemplateView):

    template_name = 'example/settings.html'
