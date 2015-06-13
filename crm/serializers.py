# -*- encoding: utf-8 -*-
from rest_framework import serializers

from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):

    contact = serializers.ReadOnlyField(source='contact.slug')
    priority = serializers.ReadOnlyField(source='priority.name')
    username = serializers.ReadOnlyField(source='user_assigned.username')

    class Meta:
        model = Ticket
        fields = (
            'contact',
            'due',
            'id',
            'priority',
            'title',
            'username',
        )
