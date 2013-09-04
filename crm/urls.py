from django.conf.urls import (
    patterns, url
)

from .views import (
    ContactDetailView,
    HomeListView,
    NoteCreateView,
    TicketCreateView,
    TicketDetailView,
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
    url(regex=r'^ticket/(?P<pk>\d+)/note/$',
        view=NoteCreateView.as_view(),
        name='crm.note.create'
        ),
    url(regex=r'^contact/(?P<slug>[-\w\d]+)/ticket/$',
        view=TicketCreateView.as_view(),
        name='crm.ticket.create'
        ),
    url(regex=r'^ticket/(?P<pk>\d+)/$',
        view=TicketDetailView.as_view(),
        name='crm.ticket.detail'
        ),
)
