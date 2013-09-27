# -*- coding: utf-8 -*-:
from resrc.utils import render_template


def home(request):
    from resrc.vote.models import Vote
    hottest_links = Vote.objects.hottest_links(limit=10, days=7)
    latest_links = Vote.objects.latest_links(limit=10, days=7)

    hottest_lists = Vote.objects.hottest_lists(limit=10, days=7)

    from taggit.models import Tag
    from django.db.models import Count
    tags = Tag.objects.select_related('links') \
        .annotate(c=Count('link')).order_by('-c') \
        .all()[:55]
    return render_template('home.html', {
        'latest_links': latest_links,
        'hottest_links': hottest_links,
        'tags': tags,
        'hottest_lists': hottest_lists,
    })


def faq(request):
    return render_template('pages/faq.html', {})


def about(request):
    return render_template('pages/about.html', {})


def listlinks(request):
    from resrc.list.models import ListLinks
    ll = ListLinks.objects.all()
    return render_template('pages/listlinks.html', {'ll': ll})
