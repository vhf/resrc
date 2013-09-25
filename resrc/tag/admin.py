# -*- coding: utf-8 -*-:
from django.contrib import admin

from resrc.tag.models import Language, RevisedTag


admin.site.register(Language)
admin.site.register(RevisedTag)
