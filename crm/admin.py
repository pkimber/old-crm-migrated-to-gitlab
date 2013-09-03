from django.contrib import admin

from .models import (
    Contact,
    Industry,
    Priority,
)


class ContactAdmin(admin.ModelAdmin):
    pass

admin.site.register(Contact, ContactAdmin)


class IndustryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Industry, IndustryAdmin)


class PriorityAdmin(admin.ModelAdmin):
    pass

admin.site.register(Priority, PriorityAdmin)
