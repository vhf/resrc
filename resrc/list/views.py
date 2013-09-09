# -*- coding: utf-8 -*-:
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
import simplejson
from urllib import urlopen

from resrc.utils import render_template
from resrc.list.models import List, ListLinks
from resrc.link.models import Link

from .forms import NewListAjaxForm, NewListForm, EditListForm


def single(request, list_pk, list_slug=None):
    alist = get_object_or_404(List, pk=list_pk)

    if list_slug is None:
        return redirect(alist)

    # avoid https://twitter.com/this_smells_fishy/status/351749761935753216
    if alist.slug != list_slug:
        raise Http404

    return render_template('lists/show_single.html', {
        'list': alist,
        'tags': alist.get_tags()[:5],
        'default_lists': ['Bookmarks', 'Reading list'],
        'request': request
    })


def ajax_add_to_list_or_create(request):
    if request.user.is_authenticated() and request.method == 'POST':
        link_pk = request.POST['lk']

        if 't' in request.POST:
            # bookmark or toread
            list_type = request.POST['t']
        else:
            list_type = 'personal'
            list_pk = request.POST['ls']

        if list_type not in ['bookmark', 'toread', 'personal']:
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
            alist, created = List.objects.get_or_create(
                title=list_title,
                owner=request.user,
                defaults={'description': description, 'is_public': False}
            )
        else:
            alist = get_object_or_404(List, pk=list_pk)

        try:
            listlink = ListLinks.objects.get(
                alist=alist,
                links=link
            )
            listlink.delete()
            data = simplejson.dumps({'result': 'removed'})
        except ListLinks.DoesNotExist:
            ListLinks.objects.create(
                alist=alist,
                links=link
            )
            data = simplejson.dumps({'result': 'added'})

        return HttpResponse(data, mimetype="application/javascript")

    else:
        data = simplejson.dumps({'result': 'fail'})
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
    if request.method != 'POST' or not request.user.is_authenticated():
        raise Http404

    form = NewListAjaxForm(link_pk, request.POST)

    if form.is_valid():
        is_private = False

        if 'private' in form.data:
            is_private = form.data['private']

        try:
            alist = List.objects.create(
                title=form.data['title'],
                description=form.data['description'],
                owner=request.user,
                is_public=not is_private
            )
            alist.save()

            link = get_object_or_404(Link, pk=link_pk)

            listlink = ListLinks.objects.create(
                alist=alist,
                links=link,
            )
            listlink.save()

            data = simplejson.dumps({'result': 'success'})
            return HttpResponse(data, mimetype="application/javascript")
        except:
            data = simplejson.dumps({'result': 'fail'})
            return HttpResponse(data, mimetype="application/javascript")
    else:
        data = simplejson.dumps({'result': 'invalid'})
        return HttpResponse(data, mimetype="application/javascript")


@login_required
def new_list(request):
    if request.method == 'POST':
        form = NewListForm(request.POST)
        if form.is_valid():
            is_private = False

            if 'private' in form.data:
                is_private = form.data['private']

            if len(form.data['url']) > 0:
                mdcontent = urlopen(form.data['url']).read()
            else:
                mdcontent = form.data['mdcontent']

            from resrc.utils.templatetags.emarkdown import listmarkdown
            alist = List.objects.create(
                title=form.data['title'],
                description=form.data['description'],
                url=form.data['url'],
                md_content=mdcontent,
                html_content=listmarkdown(mdcontent),
                owner=request.user,
                is_public=not is_private
            )
            alist.save()

            return redirect(alist.get_absolute_url())
    else:
        form = NewListForm()

    links = list(Link.objects.all())

    return render_template('lists/new_list.html', {
        'form': form,
        'links': links
    })


@login_required
def edit(request, list_pk, list_slug):
    if not request.user.is_authenticated():
        raise Http404
    alist = get_object_or_404(List, pk=list_pk)

    if request.user.pk is not alist.owner.pk:
        raise Http404

    if alist.is_public:
        private_checkbox = ''
    else:
        private_checkbox = 'checked="checked"'
    if len(alist.url) > 0:
        from_url = True
    else:
        from_url = False

    if request.method == 'POST':
        form = EditListForm(private_checkbox, alist.md_content, from_url, request.POST)
        if form.is_valid():
            is_private = False

            if 'private' in form.data:
                is_private = form.data['private']

            if len(form.data['url']) > 0:
                mdcontent = urlopen(form.data['url']).read()
            else:
                mdcontent = form.data['mdcontent']

            from resrc.utils.templatetags.emarkdown import listmarkdown

            alist.title=form.data['title'],
            alist.description=form.data['description'],
            alist.url=form.data['url'],
            alist.md_content=mdcontent,
            alist.html_content=listmarkdown(mdcontent),
            alist.is_public=not is_private

            alist.save()

            return redirect(alist.get_absolute_url())

    else:

        form = EditListForm(private_checkbox, alist.md_content, from_url, initial={
            'title': alist.title,
            'description': alist.description,
            'url': alist.url,
        })

        links = list(Link.objects.all())

        return render_template('lists/new_list.html', {
            'form': form,
            'links': links
        })
