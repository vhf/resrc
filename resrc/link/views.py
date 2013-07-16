# -*- coding: utf-8 -*-:
from django.shortcuts import get_object_or_404
from resrc.utils import render_template
from django.http import Http404

from resrc.link.models import Link


def single(request, link_pk, link_slug=None):
    '''Displays details about a profile'''
    link = get_object_or_404(Link, pk=link_pk)

    # avoid https://twitter.com/this_smells_fishy/status/351749761935753216
    if link_slug is not None and link.get_slug() != link_slug:
        raise Http404

    return render_template('links/show_single.html', {
        'link': link,
        'got': link_slug,
        'expected': link.get_slug(),
        'user': request.user
    })
