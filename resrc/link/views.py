# -*- coding: utf-8 -*-:
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from resrc.utils import render_template
from django.http import Http404

from resrc.link.models import Link
from resrc.list.models import List, ListLinks


def single(request, link_pk, link_slug=None):
    link = get_object_or_404(Link, pk=link_pk)
    titles = []

    # avoid https://twitter.com/this_smells_fishy/status/351749761935753216
    if link_slug is not None and link.get_slug() != link_slug:
        raise Http404

    if request.user.is_authenticated():
        titles = List.objects.prefetch_related('links') \
            .filter(owner=request.user, links__pk=link_pk) \
            .values_list('title', flat=True)

    return render_template('links/show_single.html', {
        'link': link,
        'user': request.user,
        'request': request,
        'titles': list(titles)
    })
