import datetime
import mptt

from django.db import models
from django.conf import settings
from django.contrib.comments.models import Comment
from django.contrib.comments.managers import CommentManager

class MpttCommentManager(CommentManager):

    def get_query_set(self):
        return super(MpttCommentManager, self).get_query_set().select_related('user')
    
    def get_root_comment(self, ctype, object_pk):
        return self.model.objects.get_or_create(
            parent = None,
            content_type = ctype,
            object_pk = str(object_pk),
            defaults = {
                'comment': 'Root comment placeholder',
                'user_name': 'Noname',
                'user_email': 'no@user.no',
                'user_url': '',
                'submit_date': datetime.datetime.now(),
                'site_id': settings.SITE_ID
            })[0]
    
    def filter_hidden_comments(self):
        """
        Match django's templatetags/comments.py behavior and hide is_public=False
        comments, and is_removed=True comments if COMMENTS_HIDE_REMOVED is True.
         
        We need it because some views (comments_more, comments_subtree...) play 
        with the queryset themselves instead of just using the templatetag  
        """
        # FIXME: We need to do something clever for those hidden comments in order
        #        not to break the displayed tree
        rval = self
        field_names = [f.name for f in self.model._meta.fields]
        if 'is_public' in field_names:
            rval = rval.filter(is_public=True)
        if getattr(settings, 'COMMENTS_HIDE_REMOVED', True) and 'is_removed' in field_names:
            rval = rval.filter(is_removed=False)
        return rval

class MpttComment(Comment):
    title = models.CharField(max_length=60)
    parent = models.ForeignKey('self', related_name='children', blank=True, null=True)
    
    def save(self, *a, **kw):
        if not self.ip_address:
            self.ip_address = '0.0.0.0'
        super(MpttComment, self).save(*a, **kw)
    
    class Meta:
        ordering = ('tree_id', 'lft')
    
    objects = MpttCommentManager()

mptt.register(MpttComment)
