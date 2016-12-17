# -*- encoding: utf-8 -*-
from django.conf.urls import url

from .views import (
    CrmContactCreateView,
    CrmContactUpdateView,
    HomeTicketListView,
    NoteCreateView,
    NoteUpdateView,
    ProjectTicketDueListView,
    ProjectTicketPriorityListView,
    TicketChildCreateView,
    TicketCompleteView,
    TicketCreateView,
    TicketDetailView,
    TicketListView,
    TicketUpdateView,
)


urlpatterns = [
    url(regex=r'^$',
        view=HomeTicketListView.as_view(),
        name='crm.ticket.home'
        ),
    # url(regex=r'^contact/(?P<slug>[-\w\d]+)/$',
    #     view=ContactDetailView.as_view(),
    #     name='crm.contact.detail'
    #     ),
    url(regex=r'^contact/(?P<slug>[-\w\d\.]+)/create/$',
        view=CrmContactCreateView.as_view(),
        name='crm.contact.create'
        ),
    url(regex=r'^contact/(?P<slug>[-\w\d\.]+)/update/$',
        view=CrmContactUpdateView.as_view(),
        name='crm.contact.update'
        ),
    url(regex=r'^ticket/(?P<pk>\d+)/note/create/$',
        view=NoteCreateView.as_view(),
        name='crm.note.create'
        ),
    url(regex=r'^note/(?P<pk>\d+)/edit/$',
        view=NoteUpdateView.as_view(),
        name='crm.note.update'
        ),
    url(regex=r'^project/ticket/due/$',
        view=ProjectTicketDueListView.as_view(),
        name='crm.project.ticket.due.list'
        ),
    url(regex=r'^project/ticket/priority/$',
        view=ProjectTicketPriorityListView.as_view(),
        name='crm.project.ticket.priority.list'
        ),
    url(regex=r'^ticket/(?P<pk>\d+)/child/create/$',
        view=TicketChildCreateView.as_view(),
        name='crm.ticket.child.create'
        ),
    url(regex=r'^ticket/(?P<pk>\d+)/complete/$',
        view=TicketCompleteView.as_view(),
        name='crm.ticket.complete'
        ),
    url(regex=r'^contact/(?P<slug>[-\w\d\.]+)/ticket/add/$',
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
]
