# -*- coding: utf-8 -*-:
from django.shortcuts import get_object_or_404
from resrc.utils import render_template
from django.http import Http404

from resrc.list.models import List


def single(request, list_pk, list_slug=None):
    '''Displays details about a profile'''
    alist = get_object_or_404(List, pk=list_pk)
    #alist = get_object_or_404(List.objects.select_related('links'), pk=list_pk)

    # avoid https://twitter.com/this_smells_fishy/status/351749761935753216
    if list_slug is not None and alist.get_slug() != list_slug:
        raise Http404

    return render_template('lists/show_single.html', {
        'list': alist
    })
