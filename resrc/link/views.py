# -*- coding: utf-8 -*-:
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import simplejson

from taggit.models import Tag

from resrc.link.models import Link
from resrc.link.forms import NewLinkForm, EditLinkForm
from resrc.list.models import List
from resrc.list.forms import NewListAjaxForm
from resrc.utils import render_template


def single(request, link_pk, link_slug=None):
    link = get_object_or_404(Link, pk=link_pk)
    titles = []
    newlistform = None

    if link_slug is None:
        return redirect(link)

    # avoid https://twitter.com/this_smells_fishy/status/351749761935753216
    if link.slug != link_slug:
        raise Http404

    if request.user.is_authenticated():
        titles = list(List.objects.all_my_list_titles(request.user, link_pk)
                      .values_list('title', flat=True))
        newlistform = NewListAjaxForm(link_pk)

    lists = List.objects.some_lists_from_link(link_pk)

    try:
        similars = link.tags.similar_objects(10)
        '''

        SELECT `taggit_taggeditem`.`content_type_id`, `taggit_taggeditem`.`object_id`, COUNT(`taggit_taggeditem`.`id`) AS `n`
        FROM `taggit_taggeditem`
        WHERE (
            NOT (`taggit_taggeditem`.`object_id` = 12 AND `taggit_taggeditem`.`content_type_id` = 16 )
            AND `taggit_taggeditem`.`tag_id` IN (SELECT DISTINCT U0.`id` FROM `taggit_tag` U0
        INNER JOIN `taggit_taggeditem` U1
            ON (U0.`id` = U1.`tag_id`)
            WHERE (U1.`object_id` = 12 AND U1.`content_type_id` = 16 ))
        ) GROUP BY `taggit_taggeditem`.`content_type_id`, `taggit_taggeditem`.`object_id`
        ORDER BY `n` DESC LIMIT 10
        '''
    except:
        similars = ''

    return render_template('links/show_single.html', {
        'link': link,
        'request': request,
        'titles': list(titles),
        'newlistform': newlistform,
        'similars': similars,
        'lists': lists
    })


@login_required
@csrf_exempt
def new_link(request):
    if request.method == 'POST':
        form = NewLinkForm(request.POST)
        if form.is_valid():
            data = form.data

            link = Link()
            link.title = data['title']
            link.url = data['url']
            from resrc.tag.models import Language
            link.language = Language.objects.get(
                language=form.data['language'])
            link.level = data['level']
            link.author = request.user

            if Link.objects.filter(url=data['url']).exists():
                return redirect(Link.objects.get(url=data['url']).get_absolute_url())

            link.save()
            list_tags = data['tags'].split(',')
            for tag in list_tags:
                link.tags.add(tag)
            link.save()

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
            alist.html_content = listmarkdown(alist.md_content, alist)
            alist.save()

            import simplejson
            data = simplejson.dumps({'result': 'added'})
            return HttpResponse(data, mimetype="application/javascript")
        else:
            if not 'ajax' in form.data:
                form = NewLinkForm()
                tags = '","'.join(
                    Tag.objects.all().values_list('name', flat=True))
                tags = '"%s"' % tags
                return render_template('links/new_link.html', {
                    'form': form,
                    'tags': tags
                })
            else:
                import simplejson
                data = simplejson.dumps({'result': 'fail'})
                return HttpResponse(data, mimetype="application/javascript")

    else:
        form = NewLinkForm()

    tags = '","'.join(Tag.objects.all().values_list('name', flat=True))
    tags = '"%s"' % tags

    return render_template('links/new_link.html', {
        'form': form,
        'tags': tags
    })


@login_required
def new_link_button(request, title='', url=''):
    form = NewLinkForm(initial={
        'title': title,
        'url': url,
    })

    tags = '","'.join(Tag.objects.all().values_list('name', flat=True))
    tags = '"%s"' % tags

    return render_template('links/new_link_button.html', {
        'form': form,
        'tags': tags
    })


@login_required
def edit_link(request, link_pk):
    link = get_object_or_404(Link, pk=link_pk)
    if request.user != link.author:
        raise Http404
    if request.method == 'POST':
        form = EditLinkForm(link_pk, request.POST)
        if form.is_valid():
            link.title = form.data['title']
            from resrc.tag.models import Language
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
            for tag in has_tags:
                if tag not in list_tags:
                    link.tags.remove(tag)
            link.save()
            return redirect(link.get_absolute_url())
        else:
            form = EditLinkForm(link_pk=link_pk, initial={
                'url': link.url,
                'title': link.title,
                'tags': ','.join([t for t in Tag.objects.filter(link=link_pk).values_list('name', flat=True)]),
                'language': link.language,
                'level': link.level
            })
            tags = '","'.join(Tag.objects.all().values_list('name', flat=True))
            tags = '"%s"' % tags
            return render_template('links/new_link.html', {
                'form': form,
                'tags': tags
            })

    else:
        form = EditLinkForm(link_pk=link_pk, initial={
            'url': link.url,
            'title': link.title,
            'tags': ','.join([t for t in Tag.objects.filter(link=link_pk).values_list('name', flat=True)]),
            'language': link.language,
            'level': link.level
        })

    tags = '","'.join(Tag.objects.all().values_list('name', flat=True))
    tags = '"%s"' % tags

    return render_template('links/new_link.html', {
        'form': form,
        'tags': tags
    })


def ajax_upvote_link(request, link_pk, list_pk=None):
    if request.user.is_authenticated() and request.method == 'POST':
        link = get_object_or_404(Link, pk=link_pk)
        from resrc.tag.models import Vote
        already_voted = Vote.objects.filter(
            user=request.user, link=link).exists()
        if not already_voted:
            link.vote(request.user, list_pk)
            data = simplejson.dumps({'result': 'success'})
            return HttpResponse(data, mimetype="application/javascript")
        else:
            data = simplejson.dumps({'result': 'fail'})
            return HttpResponse(data, mimetype="application/javascript")
    raise Http404
