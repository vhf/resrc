# -*- coding: utf-8 -*-:
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import Http404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from resrc.link.models import Link
from resrc.link.forms import NewLinkForm
from resrc.list.models import List
from resrc.list.forms import NewListForm
from resrc.utils import render_template


def single(request, link_pk, link_slug=None):
    link = get_object_or_404(Link, pk=link_pk)
    titles = []
    newlistform = None

    if link_slug is None:
        return redirect(link)

    # avoid https://twitter.com/this_smells_fishy/status/351749761935753216
    if link.get_slug() != link_slug:
        raise Http404

    if request.user.is_authenticated():
        titles = List.objects.titles_link_in(request.user, link_pk)
        newlistform = NewListForm(link_pk)

    c = {
        'link': link,
        'user': request.user,
        'request': request,
        'titles': list(titles),
        'newlistform': newlistform
    }
    return render_to_response('links/show_single.html', c, RequestContext(request))


@login_required
def new_link(request):
    '''Create a new link'''
    if request.method == 'POST':
        form = NewLinkForm(request.POST)
        if form.is_valid():
            data = form.data

            link = Link()
            link.title = data['title']
            link.url = data['url']
            link.author = request.user

            link.save()

            list_tags = data['tags'].split(',')
            for tag in list_tags:
                link.tags.add(tag)
            link.save()
            return redirect(link.get_absolute_url())
    else:
        form = NewLinkForm()

    return render_template('links/new_link.html', {
        'form': form
    })
