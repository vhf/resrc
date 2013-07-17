from django.core import urlresolvers
from django.conf import settings
from django.contrib.comments.signals import comment_was_posted
from django.conf import settings
import django.db.models

notification = False
if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
    
friends = False
if "friends" in settings.INSTALLED_APPS:
    friends = True
    from friends.models import Friendship

relationships = False
if "relationships" in settings.INSTALLED_APPS:
    relationships = True


def get_model():
    from mptt_comments.models import MpttComment
    return MpttComment

def get_form():
    from mptt_comments.forms import MpttCommentForm
    return MpttCommentForm

def get_form_target():
    return urlresolvers.reverse("mptt_comments.views.post_comment")

def comment_callback_for_notification(sender, request=None, comment=None, **kwargs):
    if not notification:
        return
        
    user = request.user
    infodict = {"user": user, "comment": comment, "object": comment.content_object }
        
    if comment.parent:
        # Comment has a parent, we'll use the _replied notices
        notice_type_suffix = "replied"
        infodict["parent_comment"] = comment.parent
        infodict["parent_comment_user"] = comment.parent.user
        
        # Additionnaly, we need to notify the user that posted the comment we
        # are replying to
        if comment.parent.user and comment.parent.user != user:
            notification.send([comment.parent.user], "comment_reply_received", infodict)
        
    else:
        notice_type_suffix = "posted"
        
    # Notifications of stuff I'm doing
    notification.send([user], "comment_%s" % (notice_type_suffix, ), infodict)
    
    # Notifications to my friends and/or my followers, except the author of the
    # parent comment, since he'll receive a separate notice anyway
    if friends:
        notification.send((x['friend'] for x in
            Friendship.objects.friends_for_user(request.user) if x['friend'] != comment.parent.user),
            "comment_friend_%s" % (notice_type_suffix, ), infodict
        )
    if relationships:
        followers = request.user.relationships.followers()
        if comment.parent and comment.parent.user:
            followers = followers.exclude(username=comment.parent.user.username)
        notification.send(followers, "comment_friend_%s" % (notice_type_suffix, ), infodict)

comment_was_posted.connect(comment_callback_for_notification)
