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

    user = request.user
    if user.is_authenticated():
        user_upvoted_lists = Vote.objects.my_upvoted_lists(user)
        user_upvoted_links = Vote.objects.my_upvoted_links(user)
    else:
        user_upvoted_lists = []
        user_upvoted_links = []

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
        'upvoted_links': user_upvoted_links,
        'upvoted_lists': user_upvoted_lists,
    })


def faq(request):
    return render_template('pages/faq.html', {})


@cache_page(60 * 15)
def about(request):
    return render_template('pages/about.html', {})


def search(request, tags=None, operand=None, excludes=None, en_only=True):
    tags_csv = cache.get('tags_csv')
    if tags_csv is None:
        from taggit.models import Tag
        tags_csv = '","'.join(Tag.objects.all().values_list('name', flat=True))
        tags_csv = '"%s"' % tags_csv
        cache.set('tags_csv', tags_csv, 60*15)
    if operand is not None:
        return render_template('pages/search.html', {
            'tags': tags_csv,
            'stags': tags,
            'sop': operand,
            'sex': excludes,
        })
    else:
        return render_template('pages/search.html', {
            'tags': tags_csv,
        })


def listlinks(request):
    from resrc.list.models import ListLinks
    ll = ListLinks.objects.all()
    return render_template('pages/listlinks.html', {'ll': ll})
