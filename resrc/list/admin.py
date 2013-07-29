# -*- coding: utf-8 -*-:
from django.contrib import admin

from resrc.list.models import List


def list_name(alist):
    return ("%s, by %s" % (alist.title, alist.owner))
list_name.short_description = 'Name'


class ListAdmin(admin.ModelAdmin):
    list_display = (list_name,)


admin.site.register(List, ListAdmin)
