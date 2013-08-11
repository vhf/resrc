# -*- coding: utf-8 -*-:
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext

from taggit.models import Tag

from resrc.link.models import Link


def single(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)

    links = Link.objects.filter(tags=tag)

    c = {
        'tag': tag,
        'links': links,
        'request': request,
    }
    return render_to_response('tags/show_single.html', c, RequestContext(request))


def index(request):
    from django.db.models import Count
    tags = Tag.objects.select_related('links') \
        .annotate(c=Count('link')).order_by('-c') \
        .all()

    c = {
        'tags': tags,
        'request': request,
    }
    return render_to_response('tags/show_index.html', c, RequestContext(request))
