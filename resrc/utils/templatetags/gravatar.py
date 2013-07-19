from django import template

import urllib
import hashlib

register = template.Library()


def gravatar(email, size=80, username=None):
    gravatar_url = "http://www.gravatar.com/avatar.php?"
    gravatar_url += urllib.urlencode({
        'gravatar_id': hashlib.md5(email).hexdigest(),
        'size': str(size)})
    if username is not None:
        return """<img src="%s" alt="gravatar for %s" />""" % (gravatar_url, username)
    else:
        return """<img src="%s" alt="gravatar" />""" % (gravatar_url)

register.simple_tag(gravatar)
