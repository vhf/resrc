# -*- coding: utf-8 -*-:
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import Http404
from django.template import RequestContext

from resrc.link.models import Link
from resrc.list.models import List
from resrc.list.forms import NewListForm


def single(request, link_pk, link_slug=None):
    link = get_object_or_404(Link, pk=link_pk)
    titles = []
    newlistform = None

    if link_slug is None:
        return redirect(link)

    # avoid https://twitter.com/this_smells_fishy/status/351749761935753216
    if link_slug is not None and link.get_slug() != link_slug:
        raise Http404

    if request.user.is_authenticated():
        titles = List.objects.prefetch_related('links') \
            .filter(owner=request.user, links__pk=link_pk) \
            .values_list('title', flat=True)
        newlistform = NewListForm(link_pk)

    c = {
        'link': link,
        'user': request.user,
        'request': request,
        'titles': list(titles),
        'newlistform': newlistform
    }
    return render_to_response('links/show_single.html', c, RequestContext(request))
