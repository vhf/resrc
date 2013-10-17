# -*- coding: utf-8 -*-:

from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
from markdown.util import etree

from django.core.urlresolvers import reverse
import re


REPLACE1_REXP = re.compile(r'[\':\?\!,/\.\+\&]+', re.UNICODE)
REPLACE2_REXP = re.compile(r'[^-\w%]', re.UNICODE)


def github_slugify(text):
    from urllib import quote_plus
    text = REPLACE1_REXP.sub('', text)
    text = quote_plus(text)
    text = REPLACE2_REXP.sub('-', text.lower())
    return text


def get_unique_slug(slug, all_slugs):
    """
    Iterates until a unique slug is found
    """
    counter = 1
    orig_slug = slug

    while True:
        if slug not in all_slugs:
            return slug

        slug = '%s-%s' % (orig_slug, counter)
        counter += 1
        if counter > 2:
            print "Alalalalaa"


def fixup(elem, alist, all_slugs):
    if elem.tag.startswith('h') and elem.tag[1] >= '1' and elem.tag[1] <= '6':
        a = etree.Element('a')
        a.text = elem.text

        slug = github_slugify(a.text)
        slug = get_unique_slug(slug, all_slugs)
        all_slugs.append(slug)

        a.set("href", '#%s' % slug)
        a.set("name", '%s' % slug)
        a.set("class", "anchor")
        elem.text = None

        elem.append(a)

    if elem.tag == "a":
        url = elem.get("href")
        internal_link = True
        if url is None or len(url) < 1:
            return all_slugs
        try:
            reverse(url)
        except:
            internal_link = False
            if url[:6] == '/link/' or url[:6] == '/list/':
                internal_link = True
            if url[0] == '#':
                internal_link = True
            if elem.get('class') == 'addthis':
                internal_link = True

        from resrc.link.models import Link
        try:
            link = Link.objects.get(url=url)
            link_exists = True
        except Link.DoesNotExist:
            link_exists = False
            try:
                if url[-1] == '/':
                    link = Link.objects.get(url=url[:-1])
                else:
                    url = url + '/'
                    link = Link.objects.get(url=url)
                link_exists = True
            except Link.DoesNotExist:
                link_exists = False

        if elem.text is not None:
            elem.text = elem.text.replace('#!uds!#', '_')
            elem.text = elem.text.replace('#!ast!#', '*')

        if not internal_link:
            if not link_exists:
                elem.set("rel", "external")  # elem.set("rel", "nofollow external")
                a = etree.Element('a')
                a.set("class", "addthis tiny button secondary")
                a.text = u'add'
                elem.append(a)
            else:
                # create link icon
                icon = etree.Element("i")
                icon.text = ""
                icon.set("class", "fi-link")

                # create link to resrc page
                newlink = etree.Element('a')
                newlink.text = elem.text + ' '  # ne pas forcer l'intitulé des liens
                newlink.set(
                    "href",
                    reverse("link-single-slug", args=(link.pk, link.slug))
                )

                elem.text = ''
                # add link icon
                elem.append(icon)
                # add link to resrc page
                elem.append(newlink)

                # add span with e.g. (book)
                span = etree.Element('span')
                span.text = link.get_categories()
                elem.append(span)

        from resrc.list.models import ListLinks
        if link_exists and alist is not None:
            listlink_exists = ListLinks.objects.filter(
                alist=alist, links=link).exists()
            if not listlink_exists:
                ListLinks.objects.create(
                    alist=alist,
                    links=link
                )
            # TODO : Store all the links parsed, compare to ListLinks, remove
            # the one not there anymore

    return all_slugs


class FixupProcessor(Treeprocessor):

    def __init__(self, alist, *args, **kwargs):
        self.alist = alist
        self.all_slugs = []

    def run(self, root):
        for child in root:
            # print self.all_slugs
            self.all_slugs = fixup(child, self.alist, self.all_slugs)
            self.run(child)

        return root


class FixupExtension(Extension):

    def __init__(self, alist):
        self.alist = alist

    def extendMarkdown(self, md, md_globals):
        md.treeprocessors.add('fixup', FixupProcessor(self.alist), '_end')
