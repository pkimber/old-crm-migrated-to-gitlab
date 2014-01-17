from django.conf.urls import (
    patterns, url
)

from .views import (
    ContactCreateView,
    ContactDetailView,
    ContactListView,
    ContactUpdateView,
    HomeTicketListView,
    NoteCreateView,
    NoteUpdateView,
    TicketCompleteView,
    TicketCreateView,
    TicketDetailView,
    TicketListView,
    TicketUpdateView,
)


urlpatterns = patterns(
    '',
    url(regex=r'^$',
        view=HomeTicketListView.as_view(),
        name='crm.ticket.home'
        ),
    url(regex=r'^contact/add/$',
        view=ContactCreateView.as_view(),
        name='crm.contact.create'
        ),
    url(regex=r'^contact/(?P<slug>[-\w\d]+)/$',
        view=ContactDetailView.as_view(),
        name='crm.contact.detail'
        ),
    url(regex=r'^contact/$',
        view=ContactListView.as_view(),
        name='crm.contact.list'
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
    url(regex=r'^ticket/(?P<pk>\d+)/complete/$',
        view=TicketCompleteView.as_view(),
        name='crm.ticket.complete'
        ),
    url(regex=r'^contact/(?P<slug>[-\w\d]+)/ticket/add/$',
        view=TicketCreateView.as_view(),
        name='crm.ticket.create'
        ),
    url(regex=r'^ticket/(?P<pk>\d+)/$',
        view=TicketDetailView.as_view(),
        name='crm.ticket.detail'
        ),
    url(regex=r'^ticket/$',
        view=TicketListView.as_view(),
        name='crm.ticket.list'
        ),
    url(regex=r'^ticket/(?P<pk>\d+)/edit/$',
        view=TicketUpdateView.as_view(),
        name='crm.ticket.update'
        ),
)
