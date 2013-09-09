# -*- coding: utf-8 -*-:
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import Http404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from taggit.models import Tag

from resrc.link.models import Link
from resrc.link.forms import NewLinkForm
from resrc.list.models import List
from resrc.list.forms import NewListAjaxForm
from resrc.utils import render_template


def single(request, link_pk, link_slug=None):
    link = get_object_or_404(Link, pk=link_pk)
    titles = []
    newlistform = None

    if link_slug is None:
        return redirect(link)

    # avoid https://twitter.com/this_smells_fishy/status/351749761935753216
    if link.slug != link_slug:
        raise Http404

    if request.user.is_authenticated():
        titles = List.objects.titles_link_in(request.user, link_pk)
        newlistform = NewListAjaxForm(link_pk)

    lists = List.objects.some_lists_from_link(link_pk)

    c = {
        'link': link,
        'user': request.user,
        'request': request,
        'titles': list(titles),
        'newlistform': newlistform,
        'lists': lists
    }
    return render_to_response('links/show_single.html', c, RequestContext(request))


@login_required
def new_link(request, url_to_add=None):
    if request.method == 'POST':
        form = NewLinkForm(request.POST)
        if form.is_valid():
            data = form.data

            link = Link()
            link.title = data['title']
            link.url = data['url']
            link.author = request.user

            if Link.objects.filter(url=data['url']).exists():
                return redirect(Link.objects.get(url=data['url']).get_absolute_url())

            link.save()

            list_tags = data['tags'].split(',')
            for tag in list_tags:
                link.tags.add(tag)
            link.save()
            return redirect(link.get_absolute_url())
    else:
        if url_to_add is not None:
            form = NewLinkForm({'url': url_to_add})
            if Link.objects.filter(url=url_to_add).exists():
                return redirect(Link.objects.get(url=data['url']).get_absolute_url())
        else:
            form = NewLinkForm()

    tags = '","'.join(Tag.objects.all().values_list('name', flat=True))
    tags = '"%s"' % tags

    return render_template('links/new_link.html', {
        'form': form,
        'tags': tags
    })

''' TODO: provide a view using Tags.similar_objects() :: https://github.com/alex/django-taggit/blob/develop/docs/api.txt
and use it for autocomplete :: https://github.com/aehlke/tag-it'''
