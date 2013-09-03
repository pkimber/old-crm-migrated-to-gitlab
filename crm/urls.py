from django.conf.urls import (
    patterns, url
)

from .views import (
    HomeListView,
    TicketCreateView,
    TicketDetailView,
)


urlpatterns = patterns(
    '',
    url(regex=r'^$',
        view=HomeListView.as_view(),
        name='crm.home'
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
