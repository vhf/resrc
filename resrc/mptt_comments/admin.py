from django.contrib import admin
from django.conf import settings
from resrc.mptt_comments.models import MpttComment
from django.utils.translation import ugettext_lazy as _


class MpttCommentsAdmin(admin.ModelAdmin):
    fieldsets = (
        (None,
         {'fields': ('content_type', 'object_pk', 'parent', 'site')}
         ),
        (_('Content'),
         {'fields':
          ('user', 'user_name', 'user_email', 'user_url', 'title', 'comment')}
         ),
        (_('Metadata'),
         {'fields': ('submit_date', 'ip_address', 'is_public', 'is_removed')}
         )
    )

    list_display = ('name', 'content_type', 'object_pk', 'ip_address',
                    'submit_date', 'is_public',   'level', 'lft', 'rght')
    list_filter = ('submit_date', 'parent', 'site', 'is_public', 'is_removed')
    date_hierarchy = 'submit_date'
    ordering = ('-submit_date',)
    search_fields = ('comment', 'user__username',
                     'user_name', 'user_email', 'user_url', 'ip_address')

admin.site.register(MpttComment, MpttCommentsAdmin)
