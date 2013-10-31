# -*- coding: utf-8 -*-:
from resrc.utils import render_template
from django.core.cache import cache
from django.views.decorators.cache import cache_page


def home(request):
    from resrc.vote.models import Vote
    hot_lk_cache = 'hot_lk_10_7'

    lang_filter = [1]
    user = request.user
    if user.is_authenticated():
        from resrc.userprofile.models import Profile
        profile = Profile.objects.get(user=user)
        lang_filter = profile.languages.all().order_by('name').values_list('pk', flat=True)
        hot_lk_cache = 'hot_lk_10_7_%s' % '_'.join(map(str, lang_filter))

        user_upvoted_links = Vote.objects.my_upvoted_links(user)
        user_upvoted_links = [x['link__pk'] for x in user_upvoted_links]
    else:
        user_upvoted_links = []

    hottest_links = cache.get(hot_lk_cache)
    if hottest_links is None:
        hottest_links = Vote.objects.hottest_links(limit=15, days=14, lang_filter=lang_filter)
        cache.set(hot_lk_cache, list(hottest_links), 60*2)

    tags_csv = cache.get('tags_csv')
    if tags_csv is None:
        from taggit.models import Tag
        tags_csv = '","'.join(Tag.objects.all().values_list('name', flat=True))
        tags_csv = '"%s"' % tags_csv
        cache.set('tags_csv', tags_csv, 60*15)

    return render_template('home.html', {
        'hottest_links': hottest_links,
        'csvtags': tags_csv,
    })


def new(request):
    from resrc.vote.models import Vote
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

    lang_filter = [1]
    if request.user.is_authenticated():
        from resrc.userprofile.models import Profile
        profile = Profile.objects.get(user=request.user)
        lang_filter = profile.languages.all().order_by('name').values_list('pk', flat=True)

    links = Vote.objects.latest_links(limit=None, days=60, lang_filter=lang_filter)

    paginator = Paginator(links, 15)
    page = request.GET.get('page')
    try:
        links = paginator.page(page)
    except PageNotAnInteger:
        links = paginator.page(1)
    except EmptyPage:
        links = paginator.page(paginator.num_pages)

    user = request.user
    if user.is_authenticated():
        user_upvoted_links = Vote.objects.my_upvoted_links(user)
        user_upvoted_links = [x['link__pk'] for x in user_upvoted_links]
    else:
        user_upvoted_links = []

    return render_template('pages/new.html', {
        'links': links,
        'upvoted_links': user_upvoted_links,
    })


@cache_page(60 * 15)
def about(request):
    return render_template('pages/about.html', {})


def search(request, tags=None, operand=None, excludes=None, lang_filter=[1]):
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


def revision(request):
    if not request.user.is_staff:
        from django.http import Http404
        raise Http404

    from resrc.link.models import RevisedLink
    revised = RevisedLink.objects.select_related('link').all()

    for rev in revised:
        rev.link.tags = ",".join(rev.link.tags.values_list('name', flat=True))

    return render_template('pages/revision.html', {
        'revised': revised,
    })
