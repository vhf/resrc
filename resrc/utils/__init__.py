# coding: utf-8

from django.shortcuts import render_to_response
from django.template import RequestContext, defaultfilters

try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()


def get_current_user():
    return getattr(_thread_locals, 'user', None)


def get_current_request():
    return getattr(_thread_locals, 'request', None)


class ThreadLocals(object):
    def process_request(self, request):
        _thread_locals.user = getattr(request, 'user', None)
        _thread_locals.request = request


def render_template(tmpl, dct=None):
    return render_to_response(
        tmpl, dct, context_instance=RequestContext(get_current_request()))


def slugify(text):
    return defaultfilters.slugify(text)
