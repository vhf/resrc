# -*- coding: utf-8 -*-:
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect
from resrc.utils import render_template
from django.http import Http404, HttpResponse
import simplejson

from resrc.list.models import List
from resrc.link.models import Link

from .forms import NewListForm


def single(request, list_pk, list_slug=None):
    alist = get_object_or_404(List, pk=list_pk)

    if list_slug is None:
        return redirect(alist)

    # avoid https://twitter.com/this_smells_fishy/status/351749761935753216
    if alist.get_slug() != list_slug:
        raise Http404

    return render_template('lists/show_single.html', {
        'list': alist,
        'default_lists': ['Bookmarks', 'Reading list']
    })


def ajax_add_to_default_list(request):
    if request.user.is_authenticated() and request.method == 'POST':
        link_pk = request.POST['lk']

        if 't' in request.POST:
            # bookmark or toread
            list_type = request.POST['t']
        else:
            list_type = 'personnal'
            list_pk = request.POST['ls']

        if list_type not in ['bookmark', 'toread', 'personnal']:
            raise Http404

        link = get_object_or_404(Link, pk=link_pk)

        if list_type in ['bookmark', 'toread']:
            list_title = None
            description = None
            if list_type == 'bookmark':
                list_title = 'Bookmarks'
                description = 'My bookmarks.'
            if list_type == 'toread':
                list_title = 'Reading list'
                description = 'My reading list.'
            try:
                alist = List.objects.get(title=list_title, owner=request.user)
            except ObjectDoesNotExist:
                alist = List.objects.create(
                    title=list_title,
                    description=description,
                    owner=request.user,
                    is_public=False,
                )
        else:
            alist = get_object_or_404(List, pk=list_pk)

        if link in alist.links.all():
            alist.links.remove(link)
            data = simplejson.dumps({'result': 'removed'})
        else :
            alist.links.add(link)
            data = simplejson.dumps({'result': 'added'})

        return HttpResponse(data, mimetype="application/javascript")

    else:
        data = simplejson.dumps({
            'result': 'fail'
        }, indent=4)
        return HttpResponse(data, mimetype="application/javascript")


def ajax_own_lists(request, link_pk):
    if not request.user.is_authenticated():
        raise Http404

    all_lists = List.objects.personal_lists(request.user)
    titles = List.objects.titles_link_in_default(request.user, link_pk)

    return render_template('lists/ajax_own_lists.html', {
        'lists': all_lists,
        'titles': titles,
        'link_pk': link_pk
    })


def ajax_create_list(request, link_pk):
    if request.method == 'POST' and request.user.is_authenticated():
        form = NewListForm(link_pk, request.POST)

        if form.is_valid():
            is_ordered = False
            is_private = False

            if 'ordered' in form.data:
                is_ordered = form.data['ordered']
            if 'private' in form.data:
                is_private = form.data['private']

            try:
                alist = List.objects.create(
                    title=form.data['title'],
                    description=form.data['description'],
                    owner=request.user,
                    is_public=not is_private,
                    is_ordered=is_ordered
                )
                alist.save()

                link = get_object_or_404(Link, pk=link_pk)

                alist.links.add(link)

                data = simplejson.dumps({
                    'result': 'success'
                }, indent=4)
                return HttpResponse(data, mimetype="application/javascript")
            except:
                data = simplejson.dumps({
                    'result': 'fail'
                }, indent=4)
                return HttpResponse(data, mimetype="application/javascript")
        else:
            data = simplejson.dumps({
                'result': 'invalid'
            }, indent=4)
            return HttpResponse(data, mimetype="application/javascript")
    else:
        raise Http404
