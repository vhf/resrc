# -*- coding: utf-8 -*-:
import markdown
import bleach
from django import template
from django.utils.safestring import mark_safe
import fixup

register = template.Library()


@register.filter(needs_autoescape=False)
def emarkdown(value):
    allowed_tags = ['div', 'span', 'p', 'pre', 'hr', 'br',
                    'strong', 'em', 'i', 'b', 'code', 'sub', 'sup',
                    'a', 'abbr', 'blockquote',
                    'ul', 'ol', 'li', 'h4', 'h5', 'h6',
                    'table', 'thead', 'tbody', 'tr', 'td', 'th']

    allowed_attrs = {
        # '*': ['class', 'id'],
        'a': ['href', 'title', 'rel', 'name', 'class'],
        'img': ['src', 'alt'],
        'i': ['class'],
    }

    md_fixup = fixup.FixupExtension(None)

    return mark_safe('{0}'.format(
        bleach.clean(
            markdown.markdown(
                value,
                extensions=[md_fixup, 'extra'],
                safe_mode='escape',
                output_format='html5'
            ),
            tags=allowed_tags,
            attributes=allowed_attrs,
        )
        .encode('utf-8')))


@register.filter(needs_autoescape=False)
def listmarkdown(value, alist):
    allowed_tags = ['div', 'span', 'p', 'pre', 'hr', 'br',
                    'strong', 'em', 'i', 'b', 'code', 'sub', 'sup',
                    'a', 'abbr', 'blockquote',
                    'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']

    allowed_attrs = {
        'a': ['href', 'title', 'rel', 'name', 'class'],
        'img': ['src', 'alt'],
        'i': ['class'],
    }

    md_fixup = fixup.FixupExtension(alist)

    return mark_safe('{0}'.format(
        bleach.clean(
            markdown.markdown(
                value,
                extensions=[md_fixup, 'extra'],
                safe_mode='escape',
                output_format='html5'
            ),
            tags=allowed_tags,
            attributes=allowed_attrs,
        )
        .encode('utf-8')))
