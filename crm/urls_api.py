# -*- encoding: utf-8 -*-
from django.conf.urls import url

from .views import TicketAPIView


urlpatterns = [
    url(regex=r'^ticket/$',
        view=TicketAPIView.as_view(),
        name='api.crm.ticket'
        ),
    url(regex=r'^ticket/(?P<pk>\d+)/$',
        view=TicketAPIView.as_view(),
        name='api.crm.ticket'
        ),
]
