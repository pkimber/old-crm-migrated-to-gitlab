from django.contrib import admin

from .models import Section, Simple


class SectionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Section, SectionAdmin)


class SimpleAdmin(admin.ModelAdmin):
    list_display = ('section', 'order', 'title', 'moderated')

admin.site.register(Simple, SimpleAdmin)
