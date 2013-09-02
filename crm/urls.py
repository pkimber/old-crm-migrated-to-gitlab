from django.conf.urls import (
    patterns, url
)

from .views import (
    HomeListView, TicketCreateView,
)


urlpatterns = patterns(
    '',
    url(regex=r'^$',
        view=HomeListView.as_view(),
        name='crm.home'
        ),
    url(regex=r'^create/$',
        view=TicketCreateView.as_view(),
        name='crm.ticket.create'
        ),
)
