from django.conf.urls import (
    patterns, url
)

from .views import HomeListView


urlpatterns = patterns(
    '',
    url(regex=r'^$',
        view=HomeListView.as_view(),
        name='crm.home'
        ),
)
