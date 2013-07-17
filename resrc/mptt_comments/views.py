import textwrap
from django import http
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Q
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.utils.html import escape
from django.utils import datastructures, simplejson
from django.http import Http404, HttpResponse

from django.contrib.comments.views.utils import next_redirect
from django.contrib.comments.views.comments import CommentPostBadRequest
from django.contrib.comments import signals, get_form, get_model

from mptt_comments.models import MpttComment


def get_ip(request):
    """
    Gets the true client IP address of the request
    Contains proxy handling involving HTTP_X_FORWARDED_FOR and multiple addresses
    """
    ip = request.META.get('REMOTE_ADDR', None)
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    return ip.replace(',', '').split()[0] # choose first of (possibly) multiple values


def new_comment(request, comment_id=None, *args, **kwargs):

    is_ajax = request.GET.get('is_ajax') and '_ajax' or ''

    if not comment_id:
        return CommentPostBadRequest("Missing comment id.")

    parent_comment = get_model().objects.get(pk=comment_id)

    target = parent_comment.content_object
    model = target.__class__

    # Construct the initial comment form
    form = get_form()(target, parent_comment=parent_comment)

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


@login_required
def post_comment(request, next=None, *args, **kwargs):
    """
    Post a comment.

    HTTP POST is required unless a initial form is requested. If ``POST['submit'] == "preview"`` or if there are
    errors a preview template, ``comments/preview.html``, will be rendered.
    """

    # Require POST
    if request.method != 'POST':
        return http.HttpResponseNotAllowed(["POST"])

    is_ajax = request.POST.get('is_ajax') and '_ajax' or ''

    # Fill out some initial data fields from an authenticated user, if present
    data = request.POST.copy()

    if request.user.is_authenticated():
        if not data.get('name', ''):
            data["name"] = request.user.get_full_name()
        if not data.get('email', ''):
            data["email"] = request.user.email

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
            parent_comment = get_model().objects.get(pk=parent_pk)
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
    form = get_form()(target, parent_comment=parent_comment, data=data)

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
                "title": form.data.get("title", ""),
                "form": form,
                "allow_post": not form.errors,
                "is_ajax": is_ajax
            },
            RequestContext(request, {})
        )

    # Otherwise create the comment
    comment = form.get_comment_object()
    comment.ip_address = get_ip(request)
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

    return next_redirect(data, next, 'comments-comment-done%s' % (is_ajax and '-ajax' or ''), c=comment._get_pk_val())

def confirmation_view(template, doc="Display a confirmation view.", is_ajax=False, *args, **kwargs):
    """
    Confirmation view generator for the "comment was
    posted/flagged/deleted/approved" views.
    """
    def confirmed(request):
        comment = None
        if 'c' in request.GET:
            try:
                comment = get_model().objects.get(pk=request.GET['c'])
            except ObjectDoesNotExist:
                pass
        return render_to_response(template, {
            'comment': comment,
            'is_ajax': is_ajax,
            'success': True
        },
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
    doc="""Display a "comment was posted" success page.""",
    is_ajax=True,
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
                "bottom_level": bottom_level,
                "is_ajax": True,
            },
            RequestContext(request, {})
        )

        return json_comments
    return {}

def comments_more(request, from_comment_pk, restrict_to_tree=False, *args, **kwargs):

    comment = get_model().objects.select_related(
        'content_type').get(pk=from_comment_pk)

    offset = getattr(settings, 'MPTT_COMMENTS_OFFSET', 20)
    collapse_above = getattr(settings, 'MPTT_COMMENTS_COLLAPSE_ABOVE', 2)
    cutoff_level = getattr(settings, 'MPTT_COMMENTS_CUTOFF', 3)
    bottom_level = 0

    qs = get_model().objects.filter_hidden_comments().filter(
        content_type=comment.content_type,
        object_pk=comment.object_pk,
        level__lte=cutoff_level
    )

    part1 = Q(tree_id=comment.tree_id) & Q(lft__gte=comment.lft + 1)
    if restrict_to_tree:
        # Here we only want the nodes with the same root-id and a greater lft
        # value.
        qs = qs.filter(part1)
        bottom_level = comment.level + 1
    else:
        # Here we need all nodes with a different root-id, or all nodes with
        # the same root-id and a greater lft value.
        # The default order should do the right thing
        #
        # FIXME: it expects tree_id to be in chronological order!
        part2 = Q(tree_id__gt=comment.tree_id)
        qs = qs.filter(part1 | part2)

    until_toplevel = []
    remaining = []
    toplevel_reached = False
    remaining_count = qs.count() - offset

    for comment in qs[:offset]:

        if comment.level == 0:
            toplevel_reached = True

        if toplevel_reached:
            remaining.append(comment)
        else:
            until_toplevel.append(comment)

    json_data = {'remaining_count': remaining_count,
                 'comments_for_update': [], 'comments_tree': {}}
    if restrict_to_tree:
        json_data['tid'] = comment.get_root().id
    else:
        json_data['tid'] = 0

    for comment in until_toplevel:
        json_comment = {'level': comment.level, 'pk':
                        comment.pk, 'parent': comment.parent_id}
        template_list = [
            "comments/display_comment.html",
        ]
        json_comment['html'] = render_to_string(
            template_list, {
                "comment": comment,
                "cutoff_level": cutoff_level,
                "collapse_levels_above": collapse_above,
                "is_ajax": True,
            },
            RequestContext(request, {})
        )
        json_data['comments_for_update'].append(json_comment)

    json_data['comments_tree'] = comment_tree_json(
        request, remaining, comment.tree_id, cutoff_level, bottom_level)

    return http.HttpResponse(simplejson.dumps(json_data), mimetype='application/json')

def comments_subtree(request, from_comment_pk, include_self=None, include_ancestors=None, *args, **kwargs):

    try:
        comment = get_model().objects.select_related(
            'content_type').get(pk=from_comment_pk)
    except get_model().DoesNotExist:
        raise Http404

    cutoff_level = comment.level + getattr(settings, 'MPTT_COMMENTS_CUTOFF', 3)
    bottom_level = not include_ancestors and (
        comment.level - (include_self and 1 or 0)) or 0

    qs = get_model().objects.filter_hidden_comments().filter(
        tree_id=comment.tree_id,
        lft__gte=comment.lft + (not include_self and 1 or 0),
        lft__lte=comment.rght,
        level__lte=cutoff_level - (include_self and 1 or 0)
    )

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
            comments = list(comment.get_ancestors()) + comments

        return render_to_response(
            template_list, {
                "comments": comments,
                "bottom_level": bottom_level,
                "cutoff_level": cutoff_level - 1,
                "collapse_levels_above": getattr(settings, 'MPTT_COMMENTS_COLLAPSE_ABOVE', 2),
                "collapse_levels_below": comment.level
            },
            RequestContext(request, {})
        )


def count_for_objects(request, content_type_id):
    """
    Returns the comment count for any object defined by content_type_id and object_id or slug.
    Mimetype defaults to plain text.
    """
    try:
        ctype = ContentType.objects.get_for_id(content_type_id)
    except ObjectDoesNotExist:
        raise Http404("No content found for id %s" % content_type_id)
    pks = request.REQUEST.getlist('pk')
    response = simplejson.dumps(dict(zip(pks,
                                         [MpttComment.objects.filter(object_pk=p, content_type=ctype).count() for p in pks])))
    return HttpResponse(response, mimetype='application/json')
