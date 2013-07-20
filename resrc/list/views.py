# -*- coding: utf-8 -*-:
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from resrc.utils import render_template
from django.http import Http404, HttpResponse
import simplejson

from resrc.list.models import List, ListLinks
from resrc.link.models import Link


def single(request, list_pk, list_slug=None):
    '''Displays details about a profile'''
    alist = get_object_or_404(List, pk=list_pk)

    # avoid https://twitter.com/this_smells_fishy/status/351749761935753216
    if list_slug is not None and alist.get_slug() != list_slug:
        raise Http404

    return render_template('lists/show_single.html', {
        'list': alist
    })


def ajax_add_to_default_list(request):
    if request.method == 'POST':
        link_pk = request.POST['lk']

        if 't' in request.POST:
            list_type = request.POST['t']  # bookmark or toread
        else:
            list_type = 'personnal'

        if list_type == 'bookmark':
            list_title = 'Bookmarks'
        if list_type == 'toread':
            list_title = 'Reading list'

        if list_type == 'bookmark' or 'toread':
            link = Link.objects.get(pk=link_pk)
            try:
                alist = List.objects.get(title=list_title, owner=request.user)
            except ObjectDoesNotExist:
                if list_type == 'bookmark':
                    alist = List.objects.create(
                        title=list_title,
                        description='My bookmarks.',
                        owner=request.user,
                        is_public=False,
                    )
                elif list_type == 'toread':
                    alist = List.objects.create(
                        title=list_title,
                        description='My reading list.',
                        owner=request.user,
                        is_public=False,
                    )

        if alist.is_ordered:
            position_in_list = alist.links.all().count() + 1
        else:
            position_in_list = 0

        listlink = None
        try:
            listlink = ListLinks.objects.get(
                alist=alist,
                links=link
            )
        except ObjectDoesNotExist:
            ListLinks.objects.create(
                alist=alist,
                links=link,
                position_in_list=position_in_list
            )
            data = simplejson.dumps({'result': 'added'})
        if listlink is not None:
            listlink.delete()
            data = simplejson.dumps({'result': 'removed'})

        return HttpResponse(data, mimetype="application/javascript")

    else:
        data = simplejson.dumps({
            'result': 'fail'
        }, indent=4)
        return HttpResponse(data, mimetype="application/javascript")
