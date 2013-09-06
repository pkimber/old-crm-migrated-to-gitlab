from django.conf.urls import (
    patterns, url
)

from .views import (
    ContactDetailView,
    ContactUpdateView,
    HomeListView,
    NoteCreateView,
    NoteUpdateView,
    TicketCreateView,
    TicketDetailView,
    TicketUpdateView,
)


urlpatterns = patterns(
    '',
    url(regex=r'^$',
        view=HomeListView.as_view(),
        name='crm.home'
        ),
    url(regex=r'^contact/(?P<slug>[-\w\d]+)/$',
        view=ContactDetailView.as_view(),
        name='crm.contact.detail'
        ),
    url(regex=r'^contact/(?P<slug>[-\w\d]+)/edit/$',
        view=ContactUpdateView.as_view(),
        name='crm.contact.update'
        ),
    url(regex=r'^ticket/(?P<pk>\d+)/note/add/$',
        view=NoteCreateView.as_view(),
        name='crm.note.create'
        ),
    url(regex=r'^note/(?P<pk>\d+)/edit/$',
        view=NoteUpdateView.as_view(),
        name='crm.note.update'
        ),
    url(regex=r'^contact/(?P<slug>[-\w\d]+)/ticket/add/$',
        view=TicketCreateView.as_view(),
        name='crm.ticket.create'
        ),
    url(regex=r'^ticket/(?P<pk>\d+)/$',
        view=TicketDetailView.as_view(),
        name='crm.ticket.detail'
        ),
    url(regex=r'^ticket/(?P<pk>\d+)/edit/$',
        view=TicketUpdateView.as_view(),
        name='crm.ticket.update'
        ),
)
