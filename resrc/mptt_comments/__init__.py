from django.core import urlresolvers


def get_model():
    from resrc.mptt_comments.models import MpttComment
    return MpttComment


def get_form():
    from resrc.mptt_comments.forms import MpttCommentForm
    return MpttCommentForm


def get_form_target():
    return urlresolvers.reverse("resrc.mptt_comments.views.post_comment")
