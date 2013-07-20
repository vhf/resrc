# -*- coding: utf-8 -*-:
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from resrc.utils import render_template
from django.http import Http404

from resrc.link.models import Link
from resrc.list.models import List, ListLinks


def single(request, link_pk, link_slug=None):
    '''Displays details about a profile'''
    link = get_object_or_404(Link, pk=link_pk)
    bookmarks = None
    toread = None

    # avoid https://twitter.com/this_smells_fishy/status/351749761935753216
    if link_slug is not None and link.get_slug() != link_slug:
        raise Http404

    if request.user.is_authenticated():
        try:
            bookmarks = list(List.objects.get(
                title='Bookmarks',
                owner=request.user
            ).links.all())
        except ObjectDoesNotExist:
            pass
        try:
            toread = list(List.objects.get(
                title='Reading list',
                owner=request.user
            ).links.all())
        except ObjectDoesNotExist:
            pass

        all_lists = List.objects.filter(owner=request.user)

        in_lists = all_lists.filter(links__pk=link_pk)
        titles = [x.title for x in in_lists]  # FIXME sql explosion \o/

        print titles

    return render_template('links/show_single.html', {
        'link': link,
        'user': request.user,
        'request': request,
        'lists': all_lists,
        'titles': titles
    })
