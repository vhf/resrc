# -*- coding: utf-8 -*-:

from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
from markdown.util import etree

from django.core.urlresolvers import reverse
import re


REPLACE1_REXP = re.compile(r'[\':\?\!,/\.\+]+', re.UNICODE)
REPLACE2_REXP = re.compile(r'[^-\w%]', re.UNICODE)


def github_slugify(text):
    from urllib import quote_plus
    text = REPLACE1_REXP.sub('', text)
    text = quote_plus(text)
    text = REPLACE2_REXP.sub('-', text.lower())
    return text

def fixup(elem, alist):
    if elem.tag.startswith('h') and elem.tag[1] >= '1' and elem.tag[1] <= '6':
        a = etree.Element('a')
        a.text = elem.text
        slug = github_slugify(a.text)
        a.set("href", '#%s' % slug)
        a.set("name", '%s' % slug)
        a.set("class", "anchor")
        elem.text = None

        elem.append(a)

    if elem.tag == "a":
        url = elem.get("href")
        internal_link = True
        if url is None or len(url) < 1:
            return
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
                    url = url+'/'
                    link = Link.objects.get(url=url)
                link_exists = True
            except Link.DoesNotExist:
                link_exists = False

        if elem.text is not None:
            elem.text = elem.text.replace('#!uds!#', '_')
            elem.text = elem.text.replace('#!ast!#', '*')

        if not internal_link:
            if not link_exists:
                elem.set("rel", "external")
                #elem.set("rel", "nofollow external")
                a = etree.Element('a')
                a.set("class", "addthis tiny button secondary")
                a.text = u'add'
                elem.append(a)
            else:
                newlink = etree.Element('a')

                icon = etree.Element("i")
                icon.text = "link "
                icon.set("class", "lsf symbol")

                # ne pas forcer l'intitulé des liens
                newlink.text = elem.text + ' '
                newlink.set(
                    "href",
                    reverse("link-single-slug", args=(link.pk, link.slug))
                )

                elem.text = ''
                elem.append(icon)
                elem.append(newlink)

        from resrc.list.models import ListLinks
        if link_exists and alist is not None:
            listlink_exists = ListLinks.objects.filter(
                alist=alist, links=link).exists()
            if not listlink_exists:
                ListLinks.objects.create(
                    alist=alist,
                    links=link
                )
            # TODO : Store all the links parsed, compare to ListLinks, remove the one not there anymore


class FixupProcessor(Treeprocessor):

    def __init__(self, alist, *args, **kwargs):
        self.alist = alist

    def run(self, root):
        for child in root:
            fixup(child, self.alist)
            self.run(child)

        return root


class FixupExtension(Extension):

    def __init__(self, alist):
        self.alist = alist

    def extendMarkdown(self, md, md_globals):
        md.treeprocessors.add('fixup', FixupProcessor(self.alist), '_end')
