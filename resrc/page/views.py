# -*- coding: utf-8 -*-:
from resrc.utils import render_template


def home(request):
    from resrc.link.models import Link
    latest_links = Link.objects.latest()

    from resrc.tag.models import Vote
    from django.db.models import Count
    from datetime import timedelta, datetime
    hottest_links = Vote.objects \
        .filter(time__gt=datetime.now()-timedelta(days=1)) \
        .exclude(link=None) \
        .values('link__pk', 'link__slug', 'link__title') \
        .annotate(count=Count('id')) \
        .order_by('-count')[:10]

    hottest_lists = Vote.objects \
        .filter(time__gt=datetime.now()-timedelta(days=1)) \
        .exclude(alist=None) \
        .values('alist__pk', 'alist__slug', 'alist__title') \
        .annotate(count=Count('id')) \
        .order_by('-count')[:10]

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
