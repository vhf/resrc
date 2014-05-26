# -*- coding: utf-8 -*-:
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect
import simplejson
import urllib2

from resrc.utils import render_template
from resrc.list.models import List, ListLinks
from resrc.link.models import Link

from .forms import NewListAjaxForm, NewListForm, EditListForm


def single(request, list_pk, list_slug=None):
    alist = get_object_or_404(List, pk=list_pk)
    alist.views = alist.views + 1
    alist.save()

    if list_slug is None:
        return redirect(alist)

    if alist.slug != list_slug:
        raise Http404
    if not alist.is_public and request.user != alist.owner:
        raise PermissionDenied

    form = None
    tags_addlink = ''

    if request.user.is_authenticated():
        from resrc.link.forms import NewLinkForm
        form = NewLinkForm(request.POST)
        from taggit.models import Tag
        tags_addlink = cache.get('tags_csv')
        if tags_addlink is None:
            from taggit.models import Tag
            tags_addlink = '","'.join(
                Tag.objects.all().values_list('name', flat=True))
            tags_addlink = '"%s"' % tags_addlink
            cache.set('tags_csv', tags_addlink, 60 * 15)

    from resrc.vote.models import Vote
    if request.user.is_authenticated():
        voted = Vote.objects.filter(alist=alist.pk, user=request.user).exists()
    else:
        voted = False
    return render_template('lists/show_single.html', {
        'form': form,
        'list': alist,
        'count': Vote.objects.votes_for_list(alist.pk),
        'voted': voted,
        'tags': alist.get_tags(),
        'tags_addlink': tags_addlink,
        'reading_list': 'Reading list',
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

        link = cache.get('link_%s' % link_pk)
        if link is None:
            link = get_object_or_404(Link, pk=link_pk)
            cache.set('link_%s' % link_pk, link, 60 * 5)

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
            listlink.remove()
            listlink.delete()
            data = simplejson.dumps({'result': 'removed'})
        except ListLinks.DoesNotExist:
            listlink = ListLinks.objects.create(
                alist=alist,
                links=link
            )
            listlink.add()
            data = simplejson.dumps({'result': 'added'})

        return HttpResponse(data, mimetype="application/javascript")

    else:
        data = simplejson.dumps({'result': 'fail'})
        return HttpResponse(data, mimetype="application/javascript")


def ajax_own_lists(request, link_pk):
    if not request.user.is_authenticated():
        raise PermissionDenied

    all_lists = List.objects.personal_lists(request.user)
    titles = list(List.objects.my_list_titles(request.user, link_pk)
                  .values_list('title', flat=True))

    return render_template('lists/ajax_own_lists.html', {
        'lists': all_lists,
        'titles': titles,
        'link_pk': link_pk
    })


def ajax_create_list(request, link_pk):
    if request.method != 'POST' or not request.user.is_authenticated():
        raise PermissionDenied

    form = NewListAjaxForm(link_pk, request.POST)

    if form.is_valid():
        is_private = False

        if 'private' in form.data:
            is_private = form.data['private']

        from resrc.language.models import Language
        lang = Language.objects.get(language=form.data['language'])

        alist = List.objects.create(
            title=form.data['title'],
            description=form.data['description'],
            owner=request.user,
            is_public=not is_private,
            language=lang,
        )

        link = cache.get('link_%s' % link_pk)
        if link is None:
            link = get_object_or_404(Link, pk=link_pk)
            cache.set('link_%s' % link_pk, link, 60 * 5)

        listlink = ListLinks.objects.create(
            alist=alist,
            links=link,
        )
        listlink.add()
        listlink.save()

        data = simplejson.dumps({'result': 'success'})
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

            if form.data['url']:
                opener = urllib2.build_opener()
                opener.addheaders = [('Accept-Charset', 'utf-8'), ('User-agent', 'Mozilla/5.0')]
                url_response = opener.open(form.data['url'])
                mdcontent = url_response.read().decode('utf-8')
            else:
                mdcontent = form.data['mdcontent']

            from resrc.language.models import Language
            try:
                lang = Language.objects.get(language=form.data['language'])
            except Language.DoesNotExist:
                lang = Language.objects.create(language=form.data['language'])

            from resrc.utils.templatetags.emarkdown import listmarkdown
            alist = List.objects.create(
                title=form.data['title'],
                description=form.data['description'],
                url=form.data['url'],
                md_content=mdcontent,
                html_content='',
                owner=request.user,
                is_public=not is_private,
                language=lang,
            )
            alist.html_content = listmarkdown(mdcontent.strip(u'\ufeff'), alist)
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
def edit(request, list_pk):
    alist = get_object_or_404(List, pk=list_pk)

    if request.user.pk != alist.owner.pk:
        raise PermissionDenied

    if alist.is_public:
        private_checkbox = ''
    else:
        private_checkbox = 'checked="checked"'
    if alist.url is not None and len(alist.url) > 0:
        from_url = True
    else:
        from_url = False

    if request.method == 'POST':
        form = EditListForm(
            private_checkbox, alist, from_url, request.POST)
        if form.is_valid():
            is_private = False

            if 'private' in form.data:
                is_private = form.data['private']

            if form.data['url']:
                opener = urllib2.build_opener()
                opener.addheaders = [('Accept-Charset', 'utf-8'), ('User-agent', 'Mozilla/5.0')]
                url_response = opener.open(form.data['url'])
                mdcontent = url_response.read().decode('utf-8')
            else:
                mdcontent = form.data['mdcontent']

            from resrc.utils.templatetags.emarkdown import listmarkdown

            from resrc.language.models import Language
            try:
                lang = Language.objects.get(language=form.data['language'])
            except Language.DoesNotExist:
                lang = Language.objects.create(language=form.data['language'])

            alist.title = form.data['title']
            alist.description = form.data['description']
            alist.url = form.data['url']
            alist.md_content = mdcontent
            alist.html_content = ''
            alist.is_public = not is_private
            alist.language = lang
            alist.save()
            # once saved, we parse the markdown to add links found to list
            alist.html_content = listmarkdown(mdcontent.strip(u'\ufeff'), alist)
            alist.save()

            return redirect(alist.get_absolute_url())

    form = EditListForm(private_checkbox, alist, from_url, initial={
        'title': alist.title,
        'description': alist.description,
        'private': not alist.is_public,
        'url': alist.url,
        'mdcontent': alist.md_content,
        'language': alist.language.language,
    })

    links = list(Link.objects.all())

    return render_template('lists/edit_list.html', {
        'list': alist,
        'form': form,
        'links': links
    })


def auto_pull(request, list_pk):
    alist = get_object_or_404(List, pk=list_pk)

    opener = urllib2.build_opener()
    opener.addheaders = [('Accept-Charset', 'utf-8'), ('User-agent', 'Mozilla/5.0')]
    url_response = opener.open(alist.url)
    mdcontent = url_response.read().decode('utf-8')


    alist.md_content = mdcontent
    alist.html_content = ''

    from resrc.utils.templatetags.emarkdown import listmarkdown
    alist.html_content = listmarkdown(mdcontent.strip(u'\ufeff'), alist)
    alist.save()

    return redirect(alist.get_absolute_url())



@login_required
def delete(request, list_pk):
    if not request.method == 'POST':
        raise PermissionDenied
    alist = get_object_or_404(List, pk=list_pk)

    if request.user.pk != alist.owner.pk:
        raise Http404

    alist.delete()
    from django.core.urlresolvers import reverse
    return redirect(reverse('user-lists', args=(request.user.username,)))


def my_lists(request, user_name):
    upvoted_count = 0
    from django.db.models import Count
    if request.user.username == user_name:
        user = request.user
        only_public = False
        owner = True
        from resrc.vote.models import Vote
        upvoted_count = len(
            list(Vote.objects.exclude(link=None).filter(user=user).values_list('pk')))

    else:
        user = get_object_or_404(User, username=user_name)
        only_public = True
        owner = False

    lists = List.objects.user_lists(user, only_public=only_public) \
        .annotate(c=Count('links'))

    return render_template('lists/lists_list.html', {
        'lists': lists,
        'owner': owner,
        'username': user_name,
        'upvoted_count': upvoted_count,
    })


def ajax_upvote_list(request, list_pk):
    if request.user.is_authenticated() and request.method == 'POST':
        alist = get_object_or_404(List, pk=list_pk)
        from resrc.vote.models import Vote
        already_voted = Vote.objects.filter(
            user=request.user, alist=alist).exists()
        cache.delete('hot_ls_10_7')
        if not already_voted:
            alist.vote(request.user)
            data = simplejson.dumps({'result': 'voted'})
            return HttpResponse(data, mimetype="application/javascript")
        else:
            alist.unvote(request.user)
            data = simplejson.dumps({'result': 'unvoted'})
            return HttpResponse(data, mimetype="application/javascript")
    raise PermissionDenied


def lists_page(request):
    from resrc.vote.models import Vote
    lang_filter = [1]
    if request.user.is_authenticated():
        from resrc.userprofile.models import Profile
        profile = Profile.objects.get(user=request.user)
        lang_filter = profile.languages.all().order_by('name').values_list('pk', flat=True)
    latest = List.objects.latest(limit=25, lang_filter=lang_filter)
    most_viewed = List.objects.most_viewed(limit=25, lang_filter=lang_filter)
    hottest = Vote.objects.hottest_lists(limit=25, days=7, lang_filter=lang_filter)
    most_voted = Vote.objects.hottest_lists(limit=25, days=30, lang_filter=lang_filter)

    if request.user.is_authenticated():
        user_upvoted = Vote.objects.my_upvoted_lists(request.user)
        user_upvoted_pk = [x['alist__pk'] for x in user_upvoted]
    else:
        user_upvoted = []
        user_upvoted_pk = []

    return render_template('lists/lists.html', {
        'latest': latest,
        'most_viewed': most_viewed,
        'hottest': hottest,
        'most_voted': most_voted,
        'upvoted': user_upvoted,
        'upvoted_pk': user_upvoted_pk,
    })
