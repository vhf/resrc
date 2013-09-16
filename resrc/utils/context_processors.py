# -*- coding: utf-8 -*-:
import sys
import django

from resrc import settings

def analytics(request):
    # Try to retrieve the Google Analytics key from settings, if any
    try:
        gak = settings.GOOGLE_ANALYTICS_KEY
    except AttributeError:
        gak = None

    return {'GOOGLE_ANALYTICS_KEY': gak}


def versions(request):
    return {
        'django_version': '{0}.{1}.{2}'.format(
            django.VERSION[0], django.VERSION[1], django.VERSION[2]),
        'python_version': '{0}.{1}.{2}'.format(
            sys.version_info[0], sys.version_info[1], sys.version_info[2])
    }
