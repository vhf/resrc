# -*- coding: utf-8 -*-:
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, HttpResponse

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
        .annotate(c=Count('link')).order_by('-c', 'name') \
        .exclude(name=None) \
        .all()
    tags = list(tags)

    return render_template('tags/show_index.html', {
        'tags' : tags
    })


def search(request, tags, operand, excludes):
    from django.db.models import Q
    import operator
    tags = tags.split(',')
    excludes = excludes.split(',')

    if tags[0] != u'':
        if operand == 'or':
            op = operator.or_
            tag_qs = reduce(op, (Q(tags__name=tag) for tag in tags))
            links = Link.objects.filter(tag_qs)
        else:
            links = Link.objects.filter(tags__name=tags[0])
            for tag in tags:
                links = links.filter(tags__name=tag)
    else:
        links = Link.objects.all()
    for exclude in excludes:
        links = links.exclude(tags__name=exclude)

    link_result = []
    links_pk = []
    for link in links:
        link_result.append({
            'pk': link.pk,
            'title': link.title,
            'url': link.get_absolute_url()
        })
        links_pk.append(link.pk)

    from resrc.list.models import List
    lists = List.objects.filter(links__in=links_pk).distinct()
    list_result = []
    for alist in lists:
        list_result.append({
            'pk': alist.pk,
            'title': alist.title,
            'url': alist.get_absolute_url()
        })

    result = []
    result.append(link_result)
    result.append(list_result)

    import simplejson
    result = simplejson.dumps(result)
    return HttpResponse(result, mimetype="application/javascript")
