# -*- coding: utf-8 -*-:
from django.shortcuts import render
from django.views.generic import View

import json

from resrc.utils import render_template
from django.contrib.admin.views.decorators import staff_member_required
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.views.decorators.cache import cache_page


class AboutView(View):
    def get(self, request):
        return render_template('pages/about.html', {})

class HomeView(View):
    def get(self, request):
        from resrc.vote.models import Vote
        hot_lk_cache = 'hot_lk_5_7'
        hot_ls_cache = 'hot_ls_14_7'
        lang_filter = [1]
        user = request.user
        if user.is_authenticated():
            from resrc.userprofile.models import Profile
            profile = Profile.objects.get(user=user)
            lang_filter = profile.languages.all().order_by('name').values_list('pk', flat=True)
            hot_lk_cache = 'hot_lk_10_30_{0}'.format('_'.join(map(str, lang_filter)))
            hot_ls_cache = 'hot_ls_10_30_{0}'.format('_'.join(map(str, lang_filter)))

            user_upvoted_lists = Vote.objects.my_upvoted_lists(user)
            user_upvoted_lists = [x['alist__pk'] for x in user_upvoted_lists]
            user_upvoted_links = Vote.objects.my_upvoted_links(user)
            user_upvoted_links = [x['link__pk'] for x in user_upvoted_links]
        else:
            user_upvoted_lists = []
            user_upvoted_links = []

        hottest_links = cache.get(hot_lk_cache)
        if hottest_links is None:
            hottest_links = Vote.objects.hottest_links(limit=5, days=30, lang_filter=lang_filter)
            cache.set(hot_lk_cache, list(hottest_links), 60*2)

        latest_links = Vote.objects.latest_links(limit=5, days=7, lang_filter=lang_filter)

        hottest_lists = cache.get(hot_ls_cache)
        if hottest_lists is None:
            hottest_lists = Vote.objects.hottest_lists(limit=5, days=30, lang_filter=lang_filter)
            cache.set(hot_ls_cache, list(hottest_lists), 60*2+2)

        tags = cache.get('tags_all')
        if tags is None:
            from taggit.models import Tag
            from django.db.models import Count
            tags = Tag.objects.select_related('links') \
                .annotate(c=Count('link')).order_by('-c') \
                .all()
            cache.set('tags_all', list(tags), 60*15)

        from taggit.models import Tag
        all_tags = Tag.objects.all().values_list('name', flat=True)
        tags_json = json.dumps([{'tag': tag} for tag in all_tags])

        return render_template('home.html', {
            'latest_links': latest_links,
            'hottest_links': hottest_links,
            'tags': tags[:22],
            'hottest_lists': hottest_lists,
            'upvoted_links': user_upvoted_links,
            'upvoted_lists': user_upvoted_lists,
            'tags_json': tags_json,
        })



def search(request, tags=None, operand=None, excludes=None, lang_filter=[1]):
    from taggit.models import Tag
    all_tags = Tag.objects.all().values_list('name', flat=True)
    tags_json = json.dumps([{'tag': tag} for tag in all_tags])

    if operand is not None:
        return render_template('pages/search.html', {
            'stags': tags,
            'sop': operand,
            'sex': excludes,
            'tags_json': tags_json,
        })
    else:
        return render_template('pages/search.html', {
            'tags_json': tags_json,
        })


def revision(request):
    if not request.user.is_staff:
        raise PermissionDenied

    from resrc.link.models import Link, RevisedLink
    revised = RevisedLink.objects.select_related('link').all()

    for rev in revised:
        rev.link.tags = ",".join(rev.link.tags.order_by('name').values_list('name', flat=True))

    links = Link.objects.filter(content=u'˘').exclude(flagged=True)

    return render_template('pages/revision.html', {
        'revised': revised,
        'links': links,
    })


@staff_member_required
def dead(request):
    return render_template('links/dead.html', {})
