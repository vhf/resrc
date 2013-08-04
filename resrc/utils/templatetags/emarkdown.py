# -*- coding: utf-8 -*-:
import markdown
import bleach
from django import template
from django.utils.safestring import mark_safe
import nofollow

register = template.Library()

md_nofollow = nofollow.NofollowExtension()

@register.filter(needs_autoescape=False)
def emarkdown(value):
    allowed_tags = ['div', 'span', 'p', 'pre', 'hr', 'br',
                    'strong', 'em', 'i', 'b', 'code', 'sub', 'sup',
                    'a', 'abbr', 'blockquote',
                    'ul', 'ol', 'li', 'h4', 'h5', 'h6',
                    'table', 'thead', 'tbody', 'tr', 'td', 'th']

    allowed_attrs = {
        # '*': ['class', 'id'],
        'a': ['href', 'title', 'rel'],
        'img': ['src', 'alt'],
    }

    return mark_safe('{0}'.format(
        bleach.clean(
            markdown.markdown(
                value,
                extensions=[md_nofollow, 'extra'],
                safe_mode='escape',
                output_format='html5'
            ),
            tags=allowed_tags,
            attributes=allowed_attrs,
        )
        .encode('utf-8')))


@register.filter(needs_autoescape=False)
def listmarkdown(value):
    allowed_tags = ['div', 'span', 'p', 'pre', 'hr', 'br',
                    'strong', 'em', 'i', 'b', 'code', 'sub', 'sup',
                    'a', 'abbr', 'blockquote',
                    'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']

    allowed_attrs = {
        # '*': ['class', 'id'],
        'a': ['href', 'title', 'rel'],
        'img': ['src', 'alt'],
    }

    return mark_safe('{0}'.format(
        bleach.clean(
            markdown.markdown(
                value,
                extensions=[md_nofollow, 'extra'],
                safe_mode='escape',
                output_format='html5'
            ),
            tags=allowed_tags,
            attributes=allowed_attrs,
        )
        .encode('utf-8')))
