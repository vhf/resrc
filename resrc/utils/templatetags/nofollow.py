# -*- coding: utf-8 -*-:
import re

from markdown.postprocessors import Postprocessor
from markdown.extensions import Extension


R_NOFOLLOW = re.compile("<(a)([^>]*href=)", re.IGNORECASE)
S_NOFOLLOW = r'<\1 rel="nofollow"\2'


class NofollowPostprocessor(Postprocessor):
    """
    TODO: Would be really nice to add nofollow only to external links
    If we do that, we could then append "external" to "nofollow" for external links.
    """
    def run(self, text):
        return R_NOFOLLOW.sub(S_NOFOLLOW, text)


class NofollowExtension(Extension):
    """ Add nofollow for links to Markdown. """
    def extendMarkdown(self, md, md_globals):
        md.postprocessors.add('nofollow', NofollowPostprocessor(md), '_end')
