# -*- coding: utf-8 -*-:
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import simplejson
from taggit.models import Tag

from resrc.utils import render_template
from resrc.link.models import Link


def single(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)

    links = Link.objects.filter(tags=tag)

    return render_template('tags/show_single.html', {
        'tag': tag,
        'links': links,
        'request': request,
    })


def index(request):
    from django.db.models import Count
    tags = Tag.objects.select_related('links') \
        .annotate(c=Count('link')).order_by('-c', 'name') \
        .exclude(name=None) \
        .all()
    tags = list(tags)

    return render_template('tags/show_index.html', {
        'tags' : tags
    })


def tokeninput_json(request):
    from resrc.utils import slugify
    from taggit.models import Tag
    from django.db.models import Count

    query = request.GET.get('q')
    result = None
    if query is None:
        #result = cache.get("tokeninput-_everything_")
        if result is None :
            tags_json = Tag.objects.all().select_related('links') \
                .annotate(freq=Count('link')) \
                .values('id', 'name', 'freq')
            result = simplejson.dumps(list(tags_json))
            cache.set("tokeninput-_everything_", result)
    else:
        #result = cache.get("tokeninput-%s" % slugify(query))
        if result is None :
            from taggit.models import Tag
            tags_json = Tag.objects.filter(name__icontains=query) \
                .select_related('links').annotate(freq=Count('link')) \
                .values('id', 'name', 'freq')
            result = simplejson.dumps(list(tags_json))
            cache.set("tokeninput-%s" % slugify(query), result)

    return HttpResponse(result, mimetype="application/javascript")


def search(request, tags, operand, excludes):

    lang_filter = [1]
    if request.user.is_authenticated():
        from resrc.userprofile.models import Profile
        profile = Profile.objects.get(user=request.user)
        lang_filter = profile.languages.all().order_by('name').values_list('pk', flat=True)
    langs = '_'.join(map(str, lang_filter))

    import hashlib
    h = hashlib.md5("%s%s%s%s" % (tags, operand, excludes, langs)).hexdigest()
    result = cache.get(h)
    if result is None:
        from django.db.models import Q
        import operator
        tags = tags.split(',')
        excludes = excludes.split(',')

        # filter after operands
        if tags[0] != u'':
            if operand == 'or':
                # clever "or" trick
                op = operator.or_
                tag_qs = reduce(op, (Q(tags__name=tag) for tag in tags))
                links = Link.objects.filter(tag_qs)
            else:
                # stupid "and" trick
                links = Link.objects.filter(tags__name=tags[0])
                for tag in tags:
                    links = links.filter(tags__name=tag)
        else:
            links = Link.objects.all()
        for exclude in excludes:
            links = links.exclude(tags__name=exclude)

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


def related(request, tags):
    tags = tags.split(',')
    related = get_related_tags(tags)[:10]
    result = simplejson.dumps(related)
    return HttpResponse(result, mimetype="application/javascript")


def get_related_tags(tags):
    # Get a QuerySet of related items : http://stackoverflow.com/questions/7021442/how-to-show-tags-related-to-a-particular-tag-in-django-taggit
    related_items = Link.objects.filter(tags__name__in=tags)

    # Get tags for those related items
    qs = Tag.objects.filter(taggit_taggeditem_items__link__in=related_items)

    # Exclude the tags we already have
    qs = qs.exclude(name__in=tags)

    from django.db.models import Count
    qs = qs.annotate(count=Count('name'))

    # Order by name and remove duplicates
    qs = qs.order_by('-count', 'name').distinct()

    # Return tag names
    return [{'tag': t.name, 'count': t.count, 'pk': t.pk} for t in list(qs)]
