# -*- encoding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from rest_framework.authtoken import views

from .views import ContactDetailView, HomeView, SettingsView


admin.autodiscover()


urlpatterns = [
    url(regex=r'^$',
        view=HomeView.as_view(),
        name='project.home'
        ),
    url(regex=r'^',
        view=include('login.urls')
        ),
    url(regex=r'^admin/',
        view=include(admin.site.urls)
        ),
    url(regex=r'^api/',
        view=include('crm.urls_api')
        ),
    url(regex=r'^contact/',
        view=include('contact.urls')
        ),
    url(regex=r'^contact/(?P<slug>[-\w\d]+)/$',
        view=ContactDetailView.as_view(),
        name='contact.detail'
        ),
    url(regex=r'^crm/',
        view=include('crm.urls')
        ),
    url(regex=r'^invoice/',
        view=include('invoice.urls')
        ),
    url(regex=r'^settings/$',
        view=SettingsView.as_view(),
        name='project.settings'
        ),
    url(regex=r'^token/$',
        view=views.obtain_auth_token,
        name='api.token.auth',
    ),
    url(r'^home/user/$',
        view=RedirectView.as_view(url=reverse_lazy('crm.ticket.home')),
        name='project.dash'
        ),
]

urlpatterns += staticfiles_urlpatterns()
