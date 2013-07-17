import textwrap
from django import http
from django.conf import settings
from django.contrib.comments.views.utils import next_redirect
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.html import escape
import resrc.mptt_comments
from django.contrib.comments import signals
from resrc.mptt_comments.models import MpttComment
from django.utils import datastructures, simplejson
from django.views.decorators.csrf import csrf_exempt


class CommentPostBadRequest(http.HttpResponseBadRequest):

    """
    Response returned when a comment post is invalid. If ``DEBUG`` is on a
    nice-ish error message will be displayed (for debugging purposes), but in
    production mode a simple opaque 400 page will be displayed.
    """

    def __init__(self, why):
        super(CommentPostBadRequest, self).__init__()
        if settings.DEBUG:
            self.content = render_to_string(
                "comments/400-debug.html", {"why": why})


def new_comment(request, comment_id=None):

    is_ajax = request.GET.get('is_ajax') and '_ajax' or ''

    if not comment_id:
        return CommentPostBadRequest("Missing comment id.")

    parent_comment = MpttComment.objects.get(pk=comment_id)

    target = parent_comment.content_object
    model = target.__class__

    # Construct the initial comment form
    form = resrc.mptt_comments.get_form()(
        target, parent_comment=parent_comment)

    template_list = [
        "comments/%s_%s_new_form%s.html" % tuple(
            str(model._meta).split(".") + [is_ajax]),
        "comments/%s_new_form%s.html" % (model._meta.app_label, is_ajax),
        "comments/new_form%s.html" % is_ajax,
    ]
    return render_to_response(
        template_list, {
            "form": form,
        },
        RequestContext(request, {})
    )


@csrf_exempt
def post_comment(request, next=None):
    """
    Post a comment.

    HTTP POST is required unless a initial form is requested. If ``POST['submit'] == "preview"`` or if there are
    errors a preview template, ``comments/preview.html``, will be rendered.
    """

    # Require POST
    if request.method != 'POST' and not get_initial_form:
        return http.HttpResponseNotAllowed(["POST"])

    is_ajax = request.POST.get('is_ajax') and '_ajax' or ''

    # Fill out some initial data fields from an authenticated user, if present
    data = request.POST.copy()

    data["user"] = request.user

    # Look up the object we're trying to comment about
    ctype = data.get("content_type")
    object_pk = data.get("object_pk")
    parent_pk = data.get("parent_pk")
    parent_comment = None
    if ctype is None or object_pk is None:
        return CommentPostBadRequest("Missing content_type or object_pk field.")
    try:
        model = models.get_model(*ctype.split(".", 1))
        target = model._default_manager.get(pk=object_pk)
        if parent_pk:
            parent_comment = MpttComment.objects.get(pk=parent_pk)
    except TypeError:
        return CommentPostBadRequest(
            "Invalid content_type value: %r" % escape(ctype))
    except AttributeError:
        return CommentPostBadRequest(
            "The given content-type %r does not resolve to a valid model." %
            escape(ctype))
    except MpttComment.DoesNotExist:
        return CommentPostBadRequest(
            "Parent comment with PK %r does not exist." %
            escape(parent_pk))
    except ObjectDoesNotExist:
        return CommentPostBadRequest(
            "No object matching content-type %r and object PK %r exists." %
            (escape(ctype), escape(object_pk)))

    # Do we want to preview the comment?
    preview = data.get("submit", "").lower() == "preview" or \
        data.get("preview", None) is not None

    # Construct the comment form
    form = resrc.mptt_comments.get_form()(
        target, parent_comment=parent_comment, data=data)

    # Check security information
    if form.security_errors():
        return CommentPostBadRequest(
            "The comment form failed security verification: %s" %
            escape(str(form.security_errors())))

    # If there are errors or if we requested a preview show the comment
    if form.errors or preview:
        template_list = [
            "comments/%s_%s_preview%s.html" % tuple(
                str(model._meta).split(".") + [is_ajax]),
            "comments/%s_preview%s.html" % (model._meta.app_label, is_ajax),
            "comments/preview%s.html" % is_ajax
        ]
        return render_to_response(
            template_list, {
                "comment": form.data.get("comment", ""),
                "form": form,
                "allow_post": not form.errors
            },
            RequestContext(request, {})
        )

    # Otherwise create the comment
    comment = form.get_comment_object()
    comment.ip_address = request.META.get("REMOTE_ADDR", None)
    if request.user.is_authenticated():
        comment.user = request.user

    # Signal that the comment is about to be saved
    responses = signals.comment_will_be_posted.send(
        sender=comment.__class__,
        comment=comment,
        request=request
    )

    for (receiver, response) in responses:
        if response == False:
            return CommentPostBadRequest(
                "comment_will_be_posted receiver %r killed the comment" % receiver.__name__)

    # Save the comment and signal that it was saved
    comment.save()
    signals.comment_was_posted.send(
        sender=comment.__class__,
        comment=comment,
        request=request
    )

    next_view = 'comments-comment-done%s' % (is_ajax and '-ajax' or '')

    return next_redirect(request, fallback=next or next_view, c=comment._get_pk_val())


def confirmation_view(template, doc="Display a confirmation view."):
    """
    Confirmation view generator for the "comment was
    posted/flagged/deleted/approved" views.
    """
    def confirmed(request):
        comment = None
        if 'c' in request.GET:
            try:
                comment = resrc.mptt_comments.get_model().objects.get(
                    pk=request.GET['c'])
            except ObjectDoesNotExist:
                pass
        return render_to_response(template,
                                  {'comment': comment},
                                  context_instance=RequestContext(request)
                                  )

    confirmed.__doc__ = textwrap.dedent("""\
        %s

        Templates: `%s``
        Context:
            comment
                The posted comment
        """ % (doc, template)
    )
    return confirmed

comment_done_ajax = confirmation_view(
    template="comments/posted_ajax.html",
    doc="""Display a "comment was posted" success page."""
)

comment_done = confirmation_view(
    template="comments/posted.html",
    doc="""Display a "comment was posted" success page."""
)



def comment_tree_json(request, object_list, tree_id, cutoff_level, bottom_level):

    if object_list:
        json_comments = {'end_level': object_list[
            -1].level, 'end_pk': object_list[-1].pk}

        template_list = [
            "comments/display_comments_tree.html",
        ]
        json_comments['html'] = render_to_string(
            template_list, {
                "comments": object_list,
                "cutoff_level": cutoff_level,
                "bottom_level": bottom_level
            },
            RequestContext(request, {})
        )

        return json_comments
    return {}


def comments_more(request, from_comment_pk):

    offset = getattr(settings, 'MPTT_COMMENTS_OFFSET', 25)

    comment = MpttComment.objects.select_related(
        'content_type').get(pk=from_comment_pk)

    cutoff_level = 3
    bottom_level = 0

    qs = MpttComment.objects.filter(
        tree_id=comment.tree_id,
        lft__gte=comment.lft + 1,
        level__gte=1,
        level__lte=cutoff_level
    ).order_by('tree_id', 'lft').select_related('user')

    until_toplevel = []
    remaining = []
    toplevel_reached = False
    remaining_count = qs.count() - offset

    for comment in qs[:offset]:

        if comment.level == 1:
            toplevel_reached = True

        if toplevel_reached:
            remaining.append(comment)
        else:
            until_toplevel.append(comment)

    json_data = {'remaining_count': remaining_count,
                 'comments_for_update': [], 'comments_tree': {}}

    for comment in until_toplevel:
        json_comment = {'level': comment.level, 'pk': comment.pk}
        template_list = [
            "comments/display_comment.html",
        ]
        json_comment['html'] = render_to_string(
            template_list, {
                "comment": comment,
                "cutoff_level": cutoff_level,
                "collapse_levels_above": 2
            },
            RequestContext(request, {})
        )
        json_data['comments_for_update'].append(json_comment)

    json_data['comments_tree'] = comment_tree_json(
        request, remaining, comment.tree_id, cutoff_level, bottom_level)

    return http.HttpResponse(simplejson.dumps(json_data), mimetype='application/json')

def comments_subtree(request, from_comment_pk, include_self=None, include_ancestors=None):

    comment = MpttComment.objects.select_related(
        'content_type').get(pk=from_comment_pk)

    cutoff_level = comment.level + getattr(settings, 'MPTT_COMMENTS_CUTOFF', 3)
    bottom_level = not include_ancestors and (
        comment.level - (include_self and 1 or 0)) or 0

    related = getattr(settings, 'MPTT_COMMENTS_SELECT_RELATED', None)

    qs = MpttComment.objects.filter(
        tree_id=comment.tree_id,
        lft__gte=comment.lft + (not include_self and 1 or 0),
        lft__lte=comment.rght,
        level__lte=cutoff_level - (include_self and 1 or 0)
    ).order_by('tree_id', 'lft')

    if related:
        qs = qs.select_related(*related)

    is_ajax = request.GET.get('is_ajax') and '_ajax' or ''

    if is_ajax:

        json_data = {'comments_for_update': [], 'comments_tree': {}}
        json_data['comments_tree'] = comment_tree_json(
            request, list(qs), comment.tree_id, cutoff_level, bottom_level)

        return http.HttpResponse(simplejson.dumps(json_data), mimetype='application/json')

    else:

        target = comment.content_object
        model = target.__class__

        template_list = [
            "comments/%s_%s_subtree.html" % tuple(str(model._meta).split(".")),
            "comments/%s_subtree.html" % model._meta.app_label,
            "comments/subtree.html"
        ]

        comments = list(qs)
        if include_ancestors:
            comments = list(comment.get_ancestors())[1:] + comments

        return render_to_response(
            template_list, {
                "comments": comments,
                "bottom_level": bottom_level,
                "cutoff_level": cutoff_level - 1,
                "collapse_levels_above": cutoff_level - (include_self and 2 or 1),
                "collapse_levels_below": comment.level

            },
            RequestContext(request, {})
        )
