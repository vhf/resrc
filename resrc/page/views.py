# -*- coding: utf-8 -*-:
from resrc.utils import render_template
from django.core.cache import cache
from django.views.decorators.cache import cache_page


def home(request):
    from resrc.vote.models import Vote
    hottest_links = cache.get('hot_lk_10_7')
    if hottest_links is None:
        hottest_links = Vote.objects.hottest_links(limit=10, days=7)
        cache.set('hot_lk_10_7', list(hottest_links), 60*3)

    latest_links = Vote.objects.latest_links(limit=10, days=7)

    hottest_lists = cache.get('hot_ls_10_7')
    if hottest_lists is None:
        hottest_lists = Vote.objects.hottest_lists(limit=10, days=7)
        cache.set('hot_ls_10_7', list(hottest_lists), 60*3+5)

    tags = cache.get('tags_all')
    if tags is None:
        from taggit.models import Tag
        from django.db.models import Count
        tags = Tag.objects.select_related('links') \
            .annotate(c=Count('link')).order_by('-c') \
            .all()
        cache.set('tags_all', list(tags), 60*15)
    return render_template('home.html', {
        'latest_links': latest_links,
        'hottest_links': hottest_links,
        'tags': tags[:55],
        'hottest_lists': hottest_lists,
    })


def faq(request):
    return render_template('pages/faq.html', {})


@cache_page(60 * 15)
def about(request):
    return render_template('pages/about.html', {})


def search(request):
    tags = cache.get('tags_csv')
    if tags is None:
        from taggit.models import Tag
        tags = '","'.join(Tag.objects.all().values_list('name', flat=True))
        tags = '"%s"' % tags
        cache.set('tags_csv', tags, 60*15)
    return render_template('pages/search.html', {
        'tags': tags,
    })


def listlinks(request):
    from resrc.list.models import ListLinks
    ll = ListLinks.objects.all()
    return render_template('pages/listlinks.html', {'ll': ll})
