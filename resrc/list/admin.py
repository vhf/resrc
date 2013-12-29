#-*- coding: utf-8 -*-:
from django.contrib import admin

from resrc.list.models import List, ListLinks


class ListLinksInline_adddate(admin.TabularInline):
    model = ListLinks
    extra = 1


class ListAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'is_public')

    def get_form(self, request, obj=None):
        self.inlines = (ListLinksInline_adddate,)
        return super(ListAdmin, self).get_form(request, obj)


admin.site.register(List, ListAdmin)
