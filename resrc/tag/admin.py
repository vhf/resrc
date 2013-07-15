# -*- coding: utf-8 -*-:
from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from resrc.tag.models import Tag


admin.site.register(Tag, MPTTModelAdmin)
