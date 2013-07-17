from django.utils.encoding import force_unicode
from django.conf import settings
from django.contrib.comments.forms import CommentForm
from django.contrib.comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from mptt_comments.models import MpttComment
from django import forms
import time
import datetime

class MpttCommentForm(CommentForm):
    title = forms.CharField()
    parent_pk = forms.IntegerField(widget=forms.HiddenInput, required=False)
    
    def __init__(self, target_object, parent_comment=None, data=None, initial=None):
        self.parent_comment = parent_comment
        super(MpttCommentForm, self).__init__(target_object, data=data, initial=initial)
        
        self.fields.keyOrder = [
            'title',
            'comment',
            'honeypot',
            'content_type',
            'object_pk',
            'timestamp',
            'security_hash',
            'parent_pk'
        ]

    def clean_title(self):
        "Truncates title to 60 chrs to avoid integrity errors"
        return self.cleaned_data['title'][:60]
    
    def get_comment_object(self):
        """
        Return a new (unsaved) comment object based on the information in this
        form. Assumes that the form is already validated and will throw a
        ValueError if not.

        Does not set any of the fields that would come from a Request object
        (i.e. ``user`` or ``ip_address``).
        """
        if not self.is_valid():
            raise ValueError("get_comment_object may only be called on valid forms")

        parent_comment = None
        parent_pk = self.cleaned_data.get("parent_pk")
        if parent_pk:
            parent_comment = MpttComment.objects.get(pk=parent_pk)
            
        new = MpttComment(
            content_type = ContentType.objects.get_for_model(self.target_object),
            object_pk    = force_unicode(self.target_object._get_pk_val()),
            user_name    = "",  # self.cleaned_data["name"],
            user_email   = "",   # self.cleaned_data["email"],
            user_url     = "",     # self.cleaned_data["url"],
            comment      = self.cleaned_data["comment"],
            submit_date  = datetime.datetime.now(),
            site_id      = settings.SITE_ID,
            is_public    = parent_comment and parent_comment.is_public or True,
            is_removed   = False,
            title        = self.cleaned_data["title"],
            parent       = parent_comment
        )

	# FIXME: maybe re-implement duplicate checking later

        return new
        
    def generate_security_data(self):
        """Generate a dict of security data for "initial" data."""
        timestamp = int(time.time())
        security_dict =   {
            'content_type'  : str(self.target_object._meta),
            'object_pk'     : str(self.target_object._get_pk_val()),
            'timestamp'     : str(timestamp),
            'security_hash' : self.initial_security_hash(timestamp),
            'parent_pk'     : self.parent_comment and str(self.parent_comment.pk) or '',
            'title'         : not self.parent_comment and force_unicode(self.target_object) or
                                u'%s%s' % ( (self.parent_comment.title[:3] != u'Re:') and 'Re: '  or u'', self.parent_comment.title)
        }
        
        return security_dict
