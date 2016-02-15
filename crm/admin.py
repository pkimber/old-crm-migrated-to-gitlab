# -*- encoding: utf-8 -*-
from django.contrib import admin

from .models import (
    # Contact,
    Industry,
    Priority,
    # UserContact,
)


# class ContactAdmin(admin.ModelAdmin):
#     pass
# 
# admin.site.register(Contact, ContactAdmin)


class IndustryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Industry, IndustryAdmin)


class PriorityAdmin(admin.ModelAdmin):
    pass

admin.site.register(Priority, PriorityAdmin)


# class UserContactAdmin(admin.ModelAdmin):
#     list_display = ('get_username', 'get_contact', 'get_contact_address')
#     ordering = ['user__username']
#
#     def get_contact(self, obj):
#         return '{}'.format(obj.contact.name)
#     get_contact.short_description = 'Contact'
#
#     def get_contact_address(self, obj):
#         return '{}'.format(obj.contact.address)
#     get_contact_address.short_description = 'Address'
#
#     def get_username(self, obj):
#         return '{}'.format(obj.user.username)
#     get_username.short_description = 'User Name'
#
# admin.site.register(UserContact, UserContactAdmin)
