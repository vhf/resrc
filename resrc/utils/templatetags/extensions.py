# -*- coding: utf-8 -*-:

from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
from markdown.util import etree

from resrc.link.models import Link
from resrc.list.models import ListLinks
from django.core.urlresolvers import reverse


def fixup(elem, alist):
    if elem.tag.startswith('h') and elem.tag[1] >= '1' and elem.tag[1] <= '6':
        classes = elem.get('class')
        if classes is not None and 'linkable' in classes:
            if len(elem[:]) > 0:
                print 'uh oh linkable header has child nodes!'
            else:
                a = etree.Element('a')
                target = '#%s' % elem.get('id')
                a.set('href', target)
                a.text = elem.text
                elem.text = None
                elem.append(a)

                icon = etree.Element('i')
                icon.set('class', 'lsf symbol')
                icon.text = 'link'
                elem.append(icon)

    if elem.tag == 'a':
        url = elem.get('href')
        internal_link = True
        try:
            reverse(url)
        except:
            internal_link = False
            if url == reverse("new-link-add", args=(url,)):
                internal_link = True
            if url[:8] == '/lk/new/':
                internal_link = True

        exists = Link.objects.filter(url=url).exists()

        if not internal_link and not exists:
            elem.set("rel", "nofollow external")
            a = etree.Element('a')
            a.set('href', reverse("new-link-add", args=(url,)))
            a.set('class', 'link-add-link')
            a.text = u'[add]'
            elem.append(a)

        if exists and alist is not None:
            ListLinks.objects.create(
                alist=alist,
                links=Link.objects.get(url=url)
            )


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
