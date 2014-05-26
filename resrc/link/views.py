# -*- coding: utf-8 -*-:
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect
import simplejson

from taggit.models import Tag

from resrc.link.models import Link
from resrc.link.forms import NewLinkForm, EditLinkForm, SuggestEditForm
from resrc.list.models import List
from resrc.list.forms import NewListAjaxForm
from resrc.utils import render_template


def single(request, link_pk, link_slug=None):
    from taggit.models import Tag
    link = cache.get('link_%s' % link_pk)
    if link is None:
        link = get_object_or_404(Link, pk=link_pk)
        cache.set('link_%s' % link_pk, link, 60*5)

    lang_filter = [1]
    if request.user.is_authenticated():
        from resrc.userprofile.models import Profile
        profile = Profile.objects.get(user=request.user)
        lang_filter = profile.languages.all().order_by('name').values_list('pk', flat=True)

    titles = []
    newlistform = None
    tags = None

    if link_slug is None:
        return redirect(link)

    if link.slug != link_slug:
        raise Http404

    reviselinkform = ''
    if request.user.is_authenticated():
        titles = list(List.objects.all_my_list_titles(request.user, link_pk)
                      .values_list('title', flat=True))
        newlistform = NewListAjaxForm(link_pk)
        reviselinkform = SuggestEditForm(link_pk, initial={
            'url': link.url,
            'title': link.title,
            'tags': ','.join([t for t in Tag.objects.filter(link=link_pk).values_list('name', flat=True)]),
            'language': link.language.language,
            'level': link.level
        })
        # for tag autocomplete
        tags = cache.get('tags_csv')
        if tags is None:
            tags = '","'.join(Tag.objects.all().values_list('name', flat=True))
            tags = '"%s"' % tags
            cache.set('tags_csv', tags, 60*15)

    lists = List.objects.some_lists_from_link(link_pk, lang_filter)

    similars = cache.get('similar_link_%s' % link_pk)
    if similars is None or True:
        similars = list()
        link_tags = list(link.tags.all())
        max_n = len(link_tags)
        if max_n > 5:
            max_n = 5
        class Enough(Exception): pass
        try:
            # n as in n-gram
            for n in xrange(max_n, 1, -1):
                n_gram = [link_tags[x:x+n] for x in xrange(len(link_tags)-n+1)]
                # iterate over all n_grams for this n
                for i in xrange(len(n_gram)):
                    tag_tuple = n_gram[i]
                    add_similars = Link.objects.filter(tags__name=link_tags[0].name)
                    for idx in xrange(1, n):
                        add_similars = add_similars.filter(tags__name=tag_tuple[idx].name)
                    add_similars = add_similars.exclude(pk=link.pk)
                    # add them to similars if not already in, do it in the right order
                    for tmp_link in add_similars:
                        if tmp_link not in similars:
                            similars.append(tmp_link)
                    if len(similars) >= 10:
                        similars = similars[:10]
                        raise Enough
        except Enough:
            pass
        cache.set('similar_link_%s' % link_pk, similars, 60*60*2)

    tldr = cache.get('tldr_%s' % link_pk)
    if tldr is None:
        try:
            from tldr.tldr import TLDRClient
            client = TLDRClient("victorfelder", "4vle5U5zqElu9xQrsoYC")
            tldr = client.searchByUrl(link.url)
        except:
            tldr = False
        cache.set('tldr_%s' % link_pk, tldr, 60*60*24*8)
    from resrc.vote.models import Vote
    if request.user.is_authenticated():
        voted = Vote.objects.filter(link=link.pk, user=request.user).exists()
    else:
        voted = False
    return render_template('links/show_single.html', {
        'link': link,
        'count': Vote.objects.votes_for_link(link.pk),
        'voted': voted,
        'request': request,
        'titles': list(titles),
        'newlistform': newlistform,
        'similars': similars,
        'tldr': tldr,
        'lists': lists,
        'reviselinkform': reviselinkform,
        'tags': tags
    })


@login_required
def new_link(request, title=None, url=None):
    if title is not None and url is not None:
        url = url.replace('http:/', 'http://')
        url = url.replace('https:/', 'https://')
        form = NewLinkForm(initial={
            'title': title,
            'url': url,
        })

        tags = cache.get('tags_csv')
        if tags is None:
            from taggit.models import Tag
            tags = '","'.join(Tag.objects.all().values_list('name', flat=True))
            tags = '"%s"' % tags
            cache.set('tags_csv', tags, 60*15)

        return render_template('links/new_link_button.html', {
            'form': form,
            'tags': tags
        })

    if request.method == 'POST':
        form = NewLinkForm(request.POST)
        if form.is_valid():
            data = form.data

            link = Link()
            link.title = data['title']
            link.url = data['url']
            from resrc.language.models import Language
            try:
                lang = Language.objects.get(language=data['language'])
            except Language.DoesNotExist:
                lang = Language.objects.create(language=data['language'])
            link.language = lang

            link.level = data['level']
            link.author = request.user

            if Link.objects.filter(url=data['url']).exists():
                return redirect(Link.objects.get(url=data['url']).get_absolute_url())

            link.save()
            list_tags = data['tags'].split(',')
            for tag in list_tags:
                link.tags.add(tag)
                cache.delete('tags_all')
                cache.delete('tags_csv')
            link.save()
            cache.set('link_%s' % link.pk, link, 60*5)

            if not 'ajax' in data:
                return redirect(link.get_absolute_url())

            alist = get_object_or_404(List, pk=data['id'])
            # if alist.owner != request.user:
            #    raise Http404
            from resrc.list.models import ListLinks
            if not ListLinks.objects.filter(alist=alist, links=link).exists():
                ListLinks.objects.create(
                    alist=alist,
                    links=link
                )
            from resrc.utils.templatetags.emarkdown import listmarkdown
            alist.html_content = listmarkdown(alist.md_content.strip(u'\ufeff'), alist)
            alist.save()

            data = simplejson.dumps({'result': 'added'})
            return HttpResponse(data, mimetype="application/javascript")
        else:
            if not 'ajax' in form.data:
                form = NewLinkForm()

                tags = cache.get('tags_csv')
                if tags is None:
                    from taggit.models import Tag
                    tags = '","'.join(Tag.objects.all().values_list('name', flat=True))
                    tags = '"%s"' % tags
                    cache.set('tags_csv', tags, 60*15)

                return render_template('links/new_link.html', {
                    'form': form,
                    'tags': tags
                })
            else:
                data = simplejson.dumps({'result': 'fail'})
                return HttpResponse(data, mimetype="application/javascript")

    else:
        form = NewLinkForm()

    tags = cache.get('tags_csv')
    if tags is None:
        from taggit.models import Tag
        tags = '","'.join(Tag.objects.all().values_list('name', flat=True))
        tags = '"%s"' % tags
        cache.set('tags_csv', tags, 60*15)

    return render_template('links/new_link.html', {
        'form': form,
        'tags': tags
    })


@login_required
def edit_link(request, link_pk):
    link = cache.get('link_%s' % link_pk)
    if link is None:
        link = get_object_or_404(Link, pk=link_pk)
        cache.set('link_%s' % link_pk, link, 60*5)
    if request.user != link.author:
        raise Http404
    if request.method == 'POST':
        form = EditLinkForm(link_pk, request.POST)
        if form.is_valid():
            link.title = form.data['title']
            from resrc.language.models import Language
            link.language = Language.objects.get(
                language=form.data['language'])
            link.level = form.data['level']
            link.author = request.user

            has_tags = link.tags.all().values_list('name', flat=True)

            link.save()
            list_tags = form.data['tags'].split(',')
            for tag in list_tags:
                if tag not in has_tags:
                    link.tags.add(tag)
                    cache.delete('tags_all')
                    cache.delete('tags_csv')
            for tag in has_tags:
                if tag not in list_tags:
                    link.tags.remove(tag)
            link.save()
            cache.set('link_%s' % link_pk, link, 60*5)
            return redirect(link.get_absolute_url())
        else:
            from taggit.models import Tag
            form = EditLinkForm(link_pk=link_pk, initial={
                'url': link.url,
                'title': link.title,
                'tags': ','.join([t for t in Tag.objects.filter(link=link_pk).values_list('name', flat=True)]),
                'language': link.language.language,
                'level': link.level
            })

            tags = cache.get('tags_csv')
            if tags is None:
                from taggit.models import Tag
                tags = '","'.join(Tag.objects.all().values_list('name', flat=True))
                tags = '"%s"' % tags
                cache.set('tags_csv', tags, 60*15)

            return render_template('links/new_link.html', {
                'edit': True,
                'form': form,
                'tags': tags
            })

    else:
        from taggit.models import Tag
        form = EditLinkForm(link_pk=link_pk, initial={
            'url': link.url,
            'title': link.title,
            'tags': ','.join([t for t in Tag.objects.filter(link=link_pk).values_list('name', flat=True)]),
            'language': link.language.language,
            'level': link.level
        })

    tags = cache.get('tags_csv')
    if tags is None:
        from taggit.models import Tag
        tags = '","'.join(Tag.objects.all().values_list('name', flat=True))
        tags = '"%s"' % tags
        cache.set('tags_csv', tags, 60*15)

    return render_template('links/new_link.html', {
        'url': link.url,
        'edit': True,
        'form': form,
        'tags': tags
    })


def ajax_upvote_link(request, link_pk, list_pk=None):
    if request.user.is_authenticated() and request.method == 'POST':
        link = cache.get('link_%s' % link_pk)
        if link is None:
            link = get_object_or_404(Link, pk=link_pk)
            cache.set('link_%s' % link_pk, link, 60*5)

        from resrc.vote.models import Vote
        already_voted = Vote.objects.filter(user=request.user, link=link).exists()
        cache.delete('hot_lk_10_7')
        if not already_voted:
            link.vote(request.user, list_pk)
            data = simplejson.dumps({'result': 'voted'})
            return HttpResponse(data, mimetype="application/javascript")
        else:
            link.unvote(request.user)
            data = simplejson.dumps({'result': 'unvoted'})
            return HttpResponse(data, mimetype="application/javascript")
    raise PermissionDenied


def ajax_revise_link(request, link_pk):
    link = cache.get('link_%s' % link_pk)
    if link is None:
        link = get_object_or_404(Link, pk=link_pk)
        cache.set('link_%s' % link_pk, link, 60*5)

    if request.user.is_authenticated() and request.method == 'POST':
        form = SuggestEditForm(link_pk, request.POST)
        data = form.data
        # we only store the differences
        title = data['title']
        if link.title == title:
            title = ''
        url = data['url']
        if link.url == url:
            url = ''
        from resrc.language.models import Language
        language = Language.objects.get(language=data['language'])
        if link.language == language:
            language = None
        level = data['level']
        if link.level == level:
            level = ''
        from resrc.link.models import RevisedLink
        rev = RevisedLink.objects.create(
            link=link,
            title=title,
            url=url,
            language=language,
            level=level,
            tags=form.data['tags']
        )
        rev.save()
        data = simplejson.dumps({'result': 'success'})
        return HttpResponse(data, mimetype="application/javascript")
    else:
        raise PermissionDenied


def links_page(request):
    from resrc.vote.models import Vote
    lang_filter = [1]
    if request.user.is_authenticated():
        from resrc.userprofile.models import Profile
        profile = Profile.objects.get(user=request.user)
        lang_filter = profile.languages.all().order_by('name').values_list('pk', flat=True)
    latest = Vote.objects.latest_links(limit=25, days=7, lang_filter=lang_filter)
    hottest = Vote.objects.hottest_links(limit=15, days=10, lang_filter=lang_filter)
    most_voted = Vote.objects.hottest_links(limit=10, days=30, lang_filter=lang_filter)

    if request.user.is_authenticated():
        user_upvoted = Vote.objects.my_upvoted_links(request.user)
        user_upvoted_pk = [x['link__pk'] for x in user_upvoted]
    else:
        user_upvoted = []
        user_upvoted_pk = []

    return render_template('links/links.html', {
        'latest': latest,
        'hottest': hottest,
        'most_voted': most_voted,
        'upvoted': user_upvoted,
        'upvoted_pk': user_upvoted_pk,
    })


@login_required
def my_links(request):
    links = Link.objects.filter(author=request.user)

    return render_template('links/my_links.html', {
        'links': links,
    })


@login_required
def upvoted_list(request):
    from resrc.vote.models import Vote
    upvoted_links = Vote.objects.my_upvoted_links(request.user)
    upvoted_lists = Vote.objects.my_upvoted_lists(request.user)

    return render_template('links/upvoted_list.html', {
        'upvoted_links': upvoted_links,
        'upvoted_lists': upvoted_lists,
    })


def search(request):
    lang_filter = [1]
    query = request.GET.get('q')
    if request.user.is_authenticated():
        from resrc.userprofile.models import Profile
        profile = Profile.objects.get(user=request.user)
        lang_filter = profile.languages.all().order_by('name').values_list('pk', flat=True)
    langs = '_'.join(map(str, lang_filter))

    import hashlib
    h = hashlib.md5("search-title-%s" % (query)).hexdigest()
    result = cache.get(h)
    if result is None:
        links = Link.objects.all()
        links = links.filter(title__icontains=query)
        links = links.filter(language__in=lang_filter)
        links = links.distinct()

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
        lists = List.objects.filter(links__in=links_pk)
        lists = lists.exclude(is_public=False)
        lists = lists.filter(language__in=lang_filter)
        lists = lists.distinct()
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
        cache.set(h, result, 60*3)

    result = simplejson.dumps(result)
    return HttpResponse(result, mimetype="application/javascript")


@staff_member_required
def dead(request,a,b):
    import httplib
    def get_status_code(host, path="/"):
        """ This function retreives the status code of a website by requesting
            HEAD data from the host. This means that it only requests the headers.
            If the host cannot be reached or something else goes wrong, it returns
            None instead.
        """
        try:
            conn = httplib.HTTPConnection(host)
            conn.request("HEAD", path)
            return conn.getresponse().status
        except StandardError:
            return None

    links = Link.objects.all()[a:b]
    result = []


    for link in links:
        from urlparse import urlparse
        url = urlparse(link.url)
        host = url.hostname
        path = url.path
        code = get_status_code(host, path)
        if str(code)[0] == "3" or str(code)[0] == "4" or str(code)[0] == "5":
            result += [{
                'id': link.id,
                'title': link.title,
                'abs_url': link.get_absolute_url(),
                'url': link.url,
                'code': code
            }]

    result = simplejson.dumps(result)
    return HttpResponse(result, mimetype="application/javascript")
