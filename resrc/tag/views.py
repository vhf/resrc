# -*- coding: utf-8 -*-:
from django.shortcuts import get_object_or_404, redirect

from taggit.models import Tag

from resrc.utils import render_template
from resrc.link.models import Link


def single(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)

    links = Link.objects.filter(tags=tag)

    return render_template('tags/show_single.html', {
        'tag': tag,
        'links': links,
        'request': request,
    })


def index(request):
    from django.db.models import Count
    tags = Tag.objects.select_related('links') \
        .annotate(c=Count('link')).order_by('-c') \
        .all()
    tags = list(tags)
    total = len(tags)
    third = float(len(tags))/float(3)
    from math import ceil, floor
    tags_col_1 = tags[0:int(ceil(third))]
    tags_col_2 = tags[int(ceil(third))+1:int(ceil(third))*2]
    tags_col_3 = tags[int(ceil(third))*2+1:]

    return render_template('tags/show_index.html', {
        'tags_col_1' : tags_col_1,
        'tags_col_2' : tags_col_2,
        'tags_col_3' : tags_col_3,
        'request': request,
    })
