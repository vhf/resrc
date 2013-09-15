# -*- coding: utf-8 -*-:

from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
from markdown.util import etree

from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from resrc.link.models import Link
from resrc.list.models import ListLinks


def fixup(elem, alist):
    if elem.tag.startswith('h') and elem.tag[1] >= '1' and elem.tag[1] <= '6':
        a = etree.Element('a')
        a.text = elem.text
        slug = slugify(a.text)
        a.set("href", '#%s' % slug)
        a.set("name", '%s' % slug)
        a.set("class", "anchor")
        elem.text = None

        icon = etree.Element("i")
        icon.text = "link"
        icon.set("class", "lsf symbol")

        elem.append(icon)
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
            if url == reverse("new-link-add", args=(url,)):
                internal_link = True
            if url[:8] == '/lk/new/':
                internal_link = True
            if url[0] == '#':
                internal_link = True
            if elem.get('class') == 'addthis':
                internal_link = True

        exists = Link.objects.filter(url=url).exists()

        if not internal_link and not exists:
            elem.set("rel", "nofollow external")
            a = etree.Element('a')
            a.set("class", "addthis")
            a.text = u'  [add]'
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
