# -*- coding: utf-8 -*-:
from django.shortcuts import get_object_or_404
from resrc.utils import render_template

from resrc.link.models import Link


def single(request, link_pk, link_slug):
    '''Displays details about a profile'''
    link = get_object_or_404(Link, pk=link_pk)


    return render_template('links/show_single.html', {
        'link': link,
        'user': request.user
    })


def detail(request):
    return render_template('page/test.html')
