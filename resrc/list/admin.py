# -*- coding: utf-8 -*-:
from django.contrib import admin

from resrc.list.models import List, ListLinks


def list_name(alist):
    return ("%s, by %s" % (alist.title, alist.owner))
list_name.short_description = 'Name'


class ListLinksInline(admin.TabularInline):
    model = ListLinks
    extra = 1
    exclude = ['position_in_list']

class ListLinksInline_ordered(admin.TabularInline):
    model = ListLinks
    extra = 1


class ListAdmin(admin.ModelAdmin):
    list_display = (list_name,)
    inlines = (ListLinksInline,)

    def get_form(self, request, obj=None):
        if obj.is_ordered:
            self.inlines = (ListLinksInline_ordered,)
        return super(ListAdmin, self).get_form(request, obj)


admin.site.register(List, ListAdmin)
